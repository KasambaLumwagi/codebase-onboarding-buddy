from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ChatSession, ChatMessage, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

print("--- Chat Sessions ---")
sessions = db.query(ChatSession).all()
for s in sessions:
    print(f"ID: {s.id}, Repo: {s.repository_id}, Created: {s.created_at}")

print("\n--- Chat Messages ---")
messages = db.query(ChatMessage).all()
for m in messages:
    print(f"ID: {m.id}, Session: {m.session_id}, Role: {m.role}, Text: {m.text[:50]}...")

if not messages:
    print("\nNO MESSAGES FOUND IN DATABASE.")
