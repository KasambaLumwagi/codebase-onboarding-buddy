import os
import google.generativeai as genai
from typing import Optional

class GeminiClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # Using gemini-2.5-flash as confirmed by user available models
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.chat = None

    def _list_available_models(self):
        try:
            print("Listing available models...")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(m.name)
        except Exception as e:
            print(f"Error listing models: {e}")

    def start_chat(self, context_text: str):
        """
        Initializes the chat with the codebase context.
        """
        # Debug: list models if this call is failing
        self._list_available_models()
        
        initial_prompt = f"""
You are an expert software engineer acting as an 'Onboarding Buddy'.
You have been provided with the entire source code of a repository below.
Your goal is to answer questions about the codebase, architecture, and implementation details.
Be concise, specific, and cite file names where possible.

CODEBASE CONTEXT:
{context_text}
"""
        # Starting chat with history is one way, or just sending the first system prompt.
        # Gemini API supports system_instruction on model init, but chat history is easier to manage here.
        # We'll treat the context as the first user message or system prompt equivalent.
        
        self.chat = self.model.start_chat(history=[
            {"role": "user", "parts": [initial_prompt]},
            {"role": "model", "parts": ["Understood. I have analyzed the codebase. Ask me anything about it."]}
        ])

    def send_message(self, message: str) -> str:
        if not self.chat:
            return "Error: Codebase not ingested yet."
        
        response = self.chat.send_message(message)
        return response.text
