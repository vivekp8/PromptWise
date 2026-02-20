import os
import numpy as np
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class EmbeddingService:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.google_key = os.getenv("GOOGLE_API_KEY")

        if self.provider == "openai" and self.openai_key:
            self.client = OpenAI(api_key=self.openai_key)
        
        if self.provider == "google" and self.google_key:
            genai.configure(api_key=self.google_key)

    def get_embeddings(self, texts: list[str]):
        if self.provider == "google":
            return self._get_google_embeddings(texts)
        else:
            return self._get_openai_embeddings(texts)

    def _get_openai_embeddings(self, texts):
        if not hasattr(self, 'client') or not self.client:
             # Fallback or error if key missing
             return None
        try:
            response = self.client.embeddings.create(input=texts, model="text-embedding-3-small")
            return [data.embedding for data in response.data]
        except Exception as e:
            print(f"OpenAI Embedding Error: {e}")
            return None

    def _get_google_embeddings(self, texts):
        if not self.google_key:
            return None
        
        results = []
        try:
            # Google's embed_content supports a list of strings for 'content'
            # However, batching implementation details can vary by SDK version.
            # Official docs suggest passing a list is supported.
            
            # Helper to embed a single batch
            def embed_batch(batch_texts):
                try:
                    result = genai.embed_content(
                        model="models/gemini-embedding-001",
                        content=batch_texts,
                        task_type="retrieval_document")
                    
                    if 'embedding' in result:
                        # Single embedding returned (if batch size 1 or API idiosyncrasy)
                        return [result['embedding']]
                    elif 'embeddings' in result:
                        # List of embeddings returned
                        return result['embeddings']
                    return []
                except Exception as batch_e:
                    print(f"Google Batch Embedding Error: {batch_e}")
                    return None

            # Attempt to embed all at once if list is small, or iterate if fails/large
            # For simplicity and robustness, we can try the list first.
            
            # If texts is a single string, wrap it
            if isinstance(texts, str):
                texts = [texts]

            # Try batching
            batch_result = embed_batch(texts)
            if batch_result and len(batch_result) == len(texts):
                 return batch_result
            
            # Fallback to iterative if batching failed or returned partial/mismatched results
            print("Fallback to iterative embedding...")
            results = []
            for text in texts:
                res = embed_batch([text])
                if res:
                    results.extend(res)
                else:
                    # If a single one fails, we might want to append a zero vector or None
                    # For now, let's just append None and filter later or handle strictly
                    print(f"Failed to embed: {text[:30]}...")
            
            return results if results else None

        except Exception as e:
            print(f"Google Embedding General Error: {e}")
            return None

embedding_service = EmbeddingService()
