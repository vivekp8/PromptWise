from datetime import datetime, timezone

USER_STORE = {
    "user123": {
        "role": "admin",
        "quota_limit": 100,
        "allowed_routes": ["Prompt_Engine"],
        "usage": 0,
    },
    "vivek": {"role": "admin"},
    "guest": {"role": "viewer"},
}


def generate_token(user_id: str) -> dict:
    issued_at = datetime.now(timezone.utc).isoformat()
    token = {"user_id": user_id, "issued_at": issued_at, "valid": True}
    return token


def verify_access(user_id: str, module_name: str) -> dict:
    user = USER_STORE.get(user_id)
    if not user:
        return {"status": "denied", "reason": "user_not_found"}

    if module_name not in user.get("allowed_routes", []):
        return {"status": "denied", "reason": "unauthorized_module"}

    if user.get("usage", 0) >= user.get("quota_limit", 0):
        return {"status": "denied", "reason": "quota_exceeded"}

    user["usage"] += 1
    return {"status": "granted", "timestamp": datetime.now(timezone.utc).isoformat()}
