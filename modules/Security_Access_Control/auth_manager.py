from datetime import datetime

USER_STORE = {
  "user123": {
    "role": "admin",
    "quota_limit": 100,
    "allowed_routes": ["Prompt_Engine"],
    "usage": 0
  }
}

def verify_access(user_id: str, module_name: str) -> dict:
    user = USER_STORE.get(user_id)
    if not user:
        return {"status": "denied", "reason": "user_not_found"}

    if module_name not in user["allowed_routes"]:
        return {"status": "denied", "reason": "unauthorized_module"}

    if user["usage"] >= user["quota_limit"]:
        return {"status": "denied", "reason": "quota_exceeded"}

    user["usage"] += 1
    return {
        "status": "granted",
        "timestamp": datetime.utcnow().isoformat()
    }
