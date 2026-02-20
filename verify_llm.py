from LLM_Provider_Orchestration.llm_client import llm_client
from modules.Prompt_Engine.embeddings import embedding_service
import os
import google.generativeai as genai

def test_provider(provider_name):
    print(f"\n--- Testing {provider_name.upper()} ---")
    # Temporarily override environment variable for the client logic if needed, 
    # but since our client reads env at init, we might need to re-init or just use the internal logic if we exposed it.
    # Actually llm_client reads env at init.
    
    # Let's manually test the SDKs to be sure, or re-instantiate client.
    
    if provider_name == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("No OpenAI API Key found.")
            return False
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )
            print("[SUCCESS] OpenAI Chat: OK")
            return True
        except Exception as e:
            print(f"[ERROR] OpenAI Chat Error: {e}")
            return False

    elif provider_name == "google":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("No Google API Key found.")
            return False
        try:
            genai.configure(api_key=api_key)
            genai.configure(api_key=api_key)
            # Using gemini-2.0-flash as listed in available models
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content("Hi")
            print("[SUCCESS] Google Gemini Chat: OK")
            return True
        except Exception as e:
            print(f"[ERROR] Google Gemini Chat Error: {e}")
            return False

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    print("Testing OpenAI...")
    openai_ok = test_provider("openai")
    print("\nTesting Google...")
    google_ok = test_provider("google")
    
    print("\n--- Recommendation ---")
    if google_ok and not openai_ok:
        print("RECOMMENDATION: Switch to Google Gemini (LLM_PROVIDER=google)")
    elif openai_ok and not google_ok:
        print("RECOMMENDATION: OpenAI is working.")
    elif openai_ok and google_ok:
         print("RECOMMENDATION: Both are working. Choose your preference.")
    else:
        print("RECOMMENDATION: Neither provider is working. Check keys.")
