# Codebase Onboarding Buddy

A Gemini-powered assistant that ingests a GitHub repository and answers questions about the codebase.

## Setup

### Backend
1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. Run: `uvicorn main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm install -D tailwindcss postcss autoprefixer` (if not already installed)
4. `npx tailwindcss init -p` (if config missing)
5. `npm run dev`

## Usage
1. Open frontend.
2. Enter Gemini API Key and Repo URL.
3. Chat with your codebase!
