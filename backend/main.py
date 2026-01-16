from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from repo_loader import clone_and_process_repo
from gemini_client import GeminiClient

load_dotenv()

app = FastAPI()

# Allow CORS for local React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global store for the active client (Single user MVP)
gemini_client: GeminiClient = None

class IngestRequest(BaseModel):
    repo_url: str
    api_key: str

class ChatRequest(BaseModel):
    message: str

@app.post("/ingest")
async def ingest_repo(request: IngestRequest):
    global gemini_client
    try:
        # Initialize client
        gemini_client = GeminiClient(api_key=request.api_key)
        
        # Process Repo
        print(f"Ingesting {request.repo_url}...")
        context_text = clone_and_process_repo(request.repo_url)
        
        # Start Chat Session
        gemini_client.start_chat(context_text)
        
        return {"status": "success", "message": "Repository ingested and analyzed."}
    except Exception as e:
        print(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    global gemini_client
    if not gemini_client:
        raise HTTPException(status_code=400, detail="Repository not ingested yet.")
    
    try:
        response = gemini_client.send_message(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
