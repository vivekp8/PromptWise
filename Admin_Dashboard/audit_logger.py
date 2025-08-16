from datetime import datetime
import json
import os

LOG_FILE = "audit_event_schema.json"

def log_event(event: str, actor: str, details: dict):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event,
        "performed_by": actor,
        "details": details
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write(json.dumps([entry], indent=2))
    else:
        with open(LOG_FILE, "r+") as f:
            logs = json.load(f)
            logs.append(entry)
            f.seek(0)
            f.write(json.dumps(logs, indent=2))