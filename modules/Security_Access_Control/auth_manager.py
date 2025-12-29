import time

# Simulated user store with quotas and access control
USER_STORE = {
    "user123": {"authorized_modules": ["Prompt_Engine"], "usage": 0, "quota": 100},
    "admin": {"authorized_modules": ["*"], "usage": 0, "quota": 1000},
}


def verify_access(user_id: str, module_name: str) -> dict:
    """
    Verifies if the user has access to a module.

    Args:
        user_id (str): ID of the user.
        module_name (str): Name of the module.

    Returns:
        dict: Access result with status and reason or timestamp.
    """
    user = USER_STORE.get(user_id)
    if not user:
        return {"status": "denied", "reason": "user_not_found"}

    if user["usage"] >= user["quota"]:
        return {"status": "denied", "reason": "quota_exceeded"}

    if "*" in user["authorized_modules"] or module_name in user["authorized_modules"]:
        user["usage"] += 1
        return {"status": "granted", "timestamp": time.time()}
    else:
        return {"status": "denied", "reason": "unauthorized_module"}


def generate_token(user_id: str) -> dict:
    """
    Generates a token for the user.

    Args:
        user_id (str): The user's ID.

    Returns:
        dict: A token with metadata.
    """
    return {"user_id": user_id, "valid": True, "issued_at": time.time()}
