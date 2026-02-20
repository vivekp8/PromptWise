import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def verify_chat():
    print("--- Verifying Chat Feature ---")
    
    # 1. Create Session
    print("Creating session...")
    try:
        res = requests.post(f"{BASE_URL}/session/create", json={"user_id": "test_user"})
        session_id = res.json()["session_id"]
        print(f"Session ID: {session_id}")
    except Exception as e:
        print(f"[FAIL] Failed to create session: {e}")
        return

    # 2. Send First Message (Context Setting)
    msg1 = "My name is PromptWiseTestBot."
    print(f"\nUser: {msg1}")
    try:
        res = requests.post(f"{BASE_URL}/chat/message", json={"session_id": session_id, "message": msg1})
        print(f"Assistant: {res.json()['content']}")
    except Exception as e:
        print(f"[FAIL] Message 1 failed: {e}")
        return

    # 3. Send Second Message (Recall)
    msg2 = "What is my name?"
    print(f"\nUser: {msg2}")
    try:
        res = requests.post(f"{BASE_URL}/chat/message", json={"session_id": session_id, "message": msg2})
        reply = res.json()['content']
        print(f"Assistant: {reply}")
        
        if "PromptWiseTestBot" in reply:
            print("[SUCCESS] Context retention verified.")
        else:
            print("[WARN] Context might not have been retained.")
    except Exception as e:
        print(f"[FAIL] Message 2 failed: {e}")
        return
        
    # 4. Check History Endpoint
    print("\nChecking History...")
    try:
        res = requests.get(f"{BASE_URL}/chat/history/{session_id}")
        history = res.json()['history']
        print(f"History length: {len(history)}")
        if len(history) >= 4: # 2 user + 2 assistant
            print("[SUCCESS] History endpoint working.")
        else:
            print("[WARN] History length mismatch.")
    except Exception as e:
        print(f"[FAIL] History check failed: {e}")

if __name__ == "__main__":
    verify_chat()
