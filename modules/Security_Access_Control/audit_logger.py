from datetime import datetime
import json
import os

# Define the path relative to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_FILE = os.path.join(BASE_DIR, "data", "audit_event_schema.json")

def log_event(event: str, user_email: str, role: str, details: dict = None):
    """
    Logs an audit event to the JSON file.
    """
    if details is None:
        details = {}

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event,
        "user_id": user_email, # Using email as user identifier for readability
        "role": role,
        "details": details,
    }

    try:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

        if not os.path.exists(LOG_FILE):
             with open(LOG_FILE, "w") as f:
                json.dump([entry], f, indent=2)
        else:
            # Read existing logs
            with open(LOG_FILE, "r+") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
                
                logs.append(entry)
                
                # Write back
                f.seek(0)
                f.truncate()
                json.dump(logs, f, indent=2)
                
    except Exception as e:
        print(f"Error logging audit event: {e}")
