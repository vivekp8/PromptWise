from fastapi import APIRouter, Depends, HTTPException
from PromptWise.utils.jwt_utils import get_current_user
import os, json

router = APIRouter(prefix="/admin/audit", tags=["Audit Logs"])
AUDIT_LOG_PATH = os.path.join("data", "audit_event_schema.json")


@router.get("/events")
def get_audit_events(user=Depends(get_current_user)):
    if user["role"] not in ["admin", "auditor"]:
        raise HTTPException(status_code=403, detail="Audit access denied")

    try:
        with open(AUDIT_LOG_PATH, "r") as f:
            logs = json.load(f)
        return {"events": logs, "requested_by": user["username"]}
    except FileNotFoundError:
        return {"events": [], "note": "No events logged yet"}
