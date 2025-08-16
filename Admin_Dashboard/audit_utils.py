import json
from datetime import datetime

def log_event(event_type, actor, target=None, extra=None):
    entry = {
        "event": event_type,
        "actor": actor,
        "target": target,
        "details": extra or "",
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        with open("PromptWise/data/audit_event_schema.json", "r+") as f:
            logs = json.load(f)
            logs.append(entry)
            f.seek(0)
            json.dump(logs, f, indent=2)
    except Exception:
        pass