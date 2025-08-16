import json
from fastapi import APIRouter

router = APIRouter()

@router.get("/admin/audit-log")
def get_audit_log():
    try:
        with open("audit_event_schema.json", "r") as f:
            logs = json.load(f)
        return logs
    except FileNotFoundError:
        return []