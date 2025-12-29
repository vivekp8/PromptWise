from modules.Security_Access_Control.auth_manager import verify_access, USER_STORE


def test_access_granted():
    USER_STORE["user123"]["usage"] = 0
    result = verify_access("user123", "Prompt_Engine")
    assert result["status"] == "granted"


def test_quota_exceeded():
    USER_STORE["user123"]["usage"] = 1000
    result = verify_access("user123", "Prompt_Engine")
    assert result["status"] == "denied"
    USER_STORE["user123"]["usage"] = 0  # reset
