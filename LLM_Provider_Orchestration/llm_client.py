import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.google_key = os.getenv("GOOGLE_API_KEY")

        print(f"DEBUG: LLMClient Initialized. Provider: {self.provider}")
        print(f"DEBUG: OpenAI Key Present: {bool(self.openai_key)}")
        print(f"DEBUG: Google Key Present: {bool(self.google_key)}")
        
        self.openai_client = None
        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
        
        if self.google_key:
            genai.configure(api_key=self.google_key, transport='rest')

    # Updated to support chat history for context
    def generate_response(self, prompt: str, history: list = None, system_prompt: str = "You are a helpful assistant.", model_name: str = "gpt-3.5-turbo"):
        history = history or []
        
        # Determine provider based on model name
        if "gemini" in model_name:
            return self._generate_google_response(prompt, history, system_prompt, model_name)
        else:
            return self._generate_openai_response(prompt, history, system_prompt, model_name)

    def _generate_openai_response(self, prompt, history, system_prompt, model_name):
        if not self.openai_client:
            return "Error: OpenAI API Key not configured."
        
        messages = [{"role": "system", "content": system_prompt}]
        # Convert history to OpenAI format
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user prompt
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.openai_client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {str(e)}"

    def _generate_google_response(self, prompt, history, system_prompt, model_name):
        if not self.google_key:
            return "Error: Google API Key not configured."
        
        try:
            model = genai.GenerativeModel(model_name)
            
            # Construct chat history for Gemini
            chat = model.start_chat(history=[
                {"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]}
                for msg in history
            ])
            
            # System prompt can be prepended to the first message or handled via config if supported
            # For now, simplest way is to prepend to current prompt or assume persona.
            # actually better to just send message.
            
            full_prompt = f"{system_prompt}\n\n{prompt}" if not history else prompt
            
            response = chat.send_message(full_prompt)
            
            # Check if response has parts (it might be blocked)
            if not response.parts:
                print(f"Gemini Response Blocked/Empty. Feedback: {response.prompt_feedback}")
                return "I'm sorry, I cannot generate a response for that prompt."
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "ResourceExhausted" in error_msg:
                return "**Service Notice**: The free AI quota has been exceeded for the moment. Please try again in a minute, or upgrade the API key."
            return f"Gemini Error: {error_msg}"

llm_client = LLMClient()
