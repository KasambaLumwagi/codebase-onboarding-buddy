from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from repo_loader import clone_and_process_repo
from gemini_client import GeminiClient
from database import engine, Base, get_db
from models import Repository, ChatSession, ChatMessage

load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global store for active clients (mapped by session_id)
# In a real app we'd load this on demand, but for MVP we cache in memory too
active_chats = {}

class IngestRequest(BaseModel):
    repo_url: str
    repo_url: str
    api_key: str = None

class ChatRequest(BaseModel):
    session_id: int
    message: str

@app.post("/ingest")
async def ingest_repo(request: IngestRequest, db: Session = Depends(get_db)):
    try:
        # Check if already exists
        repo = db.query(Repository).filter(Repository.url == request.repo_url).first()
        
        if not repo:
            print(f"Ingesting {request.repo_url}...")
            context_text = clone_and_process_repo(request.repo_url)
            repo = Repository(url=request.repo_url, context_text=context_text)
            db.add(repo)
            db.commit()
            db.refresh(repo)
        else:
            print(f"Loaded {request.repo_url} from DB.")

        # Create a new chat session
        session = ChatSession(repository_id=repo.id)
        db.add(session)
        db.commit()
        db.refresh(session)
        
        # Initialize Gemini Logic
        client = GeminiClient(api_key=request.api_key)
        client.start_chat(repo.context_text)
        
        # Store active client
        active_chats[session.id] = client
        
        return {
            "status": "success", 
            "message": "Repository ready.", 
            "session_id": session.id,
            "history": [] # New session
        }
    except Exception as e:
        print(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    session_id = request.session_id
    
    if session_id not in active_chats:
        # Try to revive session if not in memory (Optional for MVP, but good for persistence)
        # For now, let's keep it simple: if server restart, we lost the Gemini object state
        # but we can rebuild it if we have the repo context.
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found.")
        
        # We need the API key to restore. 
        # CAUTION: We didn't store API key in DB for security. 
        # So user needs to provide it again or re-ingest if session is lost from memory.
        # For this hackathon, let's assume client sends it or we fail gracefully.
        raise HTTPException(status_code=400, detail="Session expired from memory. Please re-ingest.")

    client = active_chats[session_id]
    
    # Save User Message
    user_msg_db = ChatMessage(session_id=session_id, role='user', text=request.message)
    db.add(user_msg_db)
    db.commit()

    try:
        response_text = client.send_message(request.message)
        
        # Save Model Message
        model_msg_db = ChatMessage(session_id=session_id, role='model', text=response_text)
        db.add(model_msg_db)
        db.commit()
        
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):
    # Simple endpoint to list all sessions
    sessions = db.query(ChatSession).all()
    # Return basic info
    return [{
        "id": s.id, 
        "repo": s.repository.url, 
        "date": s.created_at,
        "message_count": len(s.messages)
    } for s in sessions]

@app.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Cascade delete messages (handled by database usually, but let's be explicit if no cascade set)
    # SQLAlchemy relationship default might not delete orphans unless configured
    db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
    db.delete(session)
    db.commit()
    return {"status": "success", "message": "Session deleted"}

@app.get("/sessions/{session_id}")
def get_session_messages(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Re-hydrate the active_chats cache if missing (critical for persistence)
    # We need to restart the chat session with Gemini using the repo context
    if session_id not in active_chats:
        try:
            repo = session.repository
            # We don't have the API key stored for security, so we can't fully reconnect 
            # the Gemini client for *new* messages without asking user again.
            # But we CAN return the history for viewing.
            # For this hackathon, we'll return history. If user tries to chat, it might fail 
            # if we can't find the client. 
            pass 
        except Exception as e:
            print(f"Error restoring session: {e}")

    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()
    return {"messages": [{"role": m.role, "text": m.text} for m in messages]}

@app.get("/health")
def health_check():
    return {"status": "ok"}
