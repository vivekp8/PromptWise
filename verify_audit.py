from fastapi.testclient import TestClient
from api import app
from modules.Security_Access_Control.audit_logger import LOG_FILE
import json
import os

client = TestClient(app)

def verify_audit_logging():
    print("Verifying Audit Logging...")
    
    # 1. Clear existing logs (optional, or just read length)
    initial_count = 0
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                initial_count = len(json.load(f))
        except:
            pass

    # 2. Perform Login
    print("Simulating Admin Login...")
    response = client.post("/auth/login", json={
        "email": "admin@promptwise.com",
        "password": "adminpassword123"
    })
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return

    print("Login successful.")

    # 3. Check Logs
    if not os.path.exists(LOG_FILE):
        print(f"FAILURE: Log file {LOG_FILE} not created.")
        return

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    
    final_count = len(logs)
    
    if final_count > initial_count:
        last_entry = logs[-1]
        if last_entry["event"] == "USER_LOGIN" and last_entry["user_id"] == "admin@promptwise.com":
            print("SUCCESS: Audit log entry found.")
            print(json.dumps(last_entry, indent=2))
        else:
            print("FAILURE: Last log entry does not match expected event.")
            print(json.dumps(last_entry, indent=2))
    else:
        print("FAILURE: No new log entry added.")

if __name__ == "__main__":
    verify_audit_logging()
