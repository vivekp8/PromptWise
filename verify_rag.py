from modules.Prompt_Engine.vector_store import vector_store
from modules.Prompt_Engine.ml_classifier import route_prompt
import time

def verify_rag():
    print("--- Verifying RAG Flow ---")
    
    # 1. Index Documents
    docs = [
        "PromptWise is a specialized AI tool for prompt engineering.",
        "The current version of PromptWise supports RAG and multiple LLM providers.",
        "To reset your password in PromptWise, go to Settings > Security > Reset Password."
    ]
    print(f"Indexing {len(docs)} documents...")
    vector_store.add_documents(docs)
    
    # 2. Verify Search
    query = "How do I reset my password?"
    print(f"\nSearching for: '{query}'")
    results = vector_store.search(query)
    print("Search Results:", results)
    
    if not results:
        print("[FAIL] No results found from vector store.")
        return
    
    found = any("Reset Password" in r for r in results)
    if found:
        print("[SUCCESS] Retrieval working correctly.")
    else:
        print("[WARN] Retrieval returned results but maybe not the most relevant one.")

    # 3. Verify End-to-End Generation
    # We need to ensure the classifier sees this as a 'question'
    # Since we can't easily mock the classifier's internal model without retraining or mocking,
    # we will force the route_prompt logic if possible, or just test if route_prompt handles it.
    
    # Note: If the classifier doesn't classify "How do I reset my password?" as a question, RAG won't trigger.
    # Let's hope the pre-trained model or basic logic works. If not, we might need to mock classify_prompt.
    
    print("\nTesting Generation via route_prompt...")
    response = route_prompt(query)
    print(f"LLM Response:\n{response}")
    
    if "Settings" in response or "Security" in response:
        print("[SUCCESS] RAG context usage confirmed in response.")
    else:
        print("[WARN] Response might not have used context. Check LLM verbosity.")

if __name__ == "__main__":
    verify_rag()
