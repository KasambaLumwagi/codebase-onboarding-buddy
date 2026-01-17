import os
import google.generativeai as genai
from typing import Optional

class GeminiClient:
    def __init__(self, api_key: str = None):
        key_to_use = api_key or os.environ.get("GEMINI_API_KEY")
        if not key_to_use:
            raise ValueError("API Key not found. Please set GEMINI_API_KEY env var or pass it explicitly.")
        genai.configure(api_key=key_to_use)
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

    def start_chat(self, context_text: str, custom_history: list = None):
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
        
        final_history = []
        if custom_history:
            # Prepend context as system prompt equivalent in first user message
            # But since gemini history is strict (User, Model, User, Model...),
            # we need to be careful. If we are restoring, we should assume the
            # first message in custom_history IS the context or we need to prepend it.
            # Simpler approach: Just use custom_history if provided, assuming it's valid.
            # BETTER APPROACH: Add context as a separate history item if not present?
            # For simplicity in this MVP: We re-initialize freshly with context,
            # then append the rest of the history? No, API expects history at init.
            
            # Re-inserting context at the start of history
            final_history = [
                 {"role": "user", "parts": [initial_prompt]},
                 {"role": "model", "parts": ["Understood. I have analyzed the codebase. Ask me anything about it."]}
            ] + custom_history
        else:
            final_history = [
                {"role": "user", "parts": [initial_prompt]},
                {"role": "model", "parts": ["Understood. I have analyzed the codebase. Ask me anything about it."]}
            ]
        
        self.chat = self.model.start_chat(history=final_history)

    def send_message(self, message: str) -> str:
        if not self.chat:
            return "Error: Codebase not ingested yet."
        
        response = self.chat.send_message(message)
        return response.text
