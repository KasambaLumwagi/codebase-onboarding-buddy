# Codebase Onboarding Buddy 🚀

A powerful, **Gemini 2.5 Flash**-powered assistant that ingests entire GitHub repositories and serves as an interactive pair-programming partner. It uses Gemini's massive context window to "read" the whole codebase, allowing it to answer complex architectural questions that standard RAG pipelines miss.

![Demo](https://via.placeholder.com/800x400?text=Codebase+Onboarding+Buddy+Demo)

## ✨ Features

- **Full Context Ingestion**: Uses Gemini 2.5 Flash to analyze the repository as a whole, not just snippets.
- **Instant Onboarding**: Paste a GitHub URL and start asking "Where is the auth logic?" in seconds.
- **Smart Filtering**: Automatically ignores lock files and binary assets to optimize context window usage.
- **Visual History**: SQLite-backed sidebar to manage multiple repository chat sessions.
- **Privacy-First**: Runs locally; your API key is used directly from your machine.

## 🛠️ Tech Stack

- **AI Model**: Google Gemini 2.5 Flash
- **Backend**: FastAPI (Python), SQLAlchemy (SQLite)
- **Frontend**: React, Vite, Tailwind CSS

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- A Google Gemini API Key

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```
*Backend will start on http://localhost:8000*

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Frontend will start on http://localhost:5173*

## 💡 Usage

1. Open `http://localhost:5173` in your browser.
2. Enter your **Gemini API Key** and a **GitHub Repository URL** (e.g., `https://github.com/fastapi/fastapi`).
3. Click **Start Onboarding**.
4. Ask questions like:
   - "How is the database connection handled?"
   - "Refactor the user model to add a phone number field."
   - "Explain the directory structure."

## 🎥 Video Demo
[Link to your YouTube/Drive video here]

---
*Built for the Gemini 3 Hackathon*
