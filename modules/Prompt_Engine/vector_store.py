import faiss
import numpy as np
import os
from modules.Prompt_Engine.embeddings import embedding_service

class VectorStore:
    def __init__(self):
        # Determine dimension based on provider
        if embedding_service.provider == "google":
            self.dimension = 768 # models/gemini-embedding-001
        else:
            self.dimension = 1536 # text-embedding-3-small
            
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []

    def add_documents(self, docs: list[str]):
        if not docs:
            return
        
        embeddings = embedding_service.get_embeddings(docs)
        if embeddings:
            # Handle potential object arrays or lists
            try:
                embeddings_np = np.array(embeddings).astype('float32')
                self.index.add(embeddings_np)
                self.documents.extend(docs)
                print(f"Added {len(docs)} documents to vector store.")
            except Exception as e:
                print(f"Error adding to index: {e}")

    def search(self, query: str, k: int = 3):
        if self.index.ntotal == 0:
            return []
        
        query_embedding = embedding_service.get_embeddings([query])
        if query_embedding:
            query_np = np.array(query_embedding).astype('float32')
            distances, indices = self.index.search(query_np, k)
            
            results = []
            for idx in indices[0]:
                if idx != -1 and idx < len(self.documents):
                    results.append(self.documents[idx])
            return results
        return []

vector_store = VectorStore()
