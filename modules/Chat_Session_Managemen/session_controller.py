from datetime import datetime

sessions = {}

def start_session(user_id: str) -> dict:
    session_id = f"{user_id}_{int(datetime.utcnow().timestamp())}"
    sessions[session_id] = {
        "user_id": user_id,
        "start_time": datetime.utcnow().isoformat(),
        "status": "active",
        "history": []
    }
    return sessions[session_id]

def end_session(session_id: str) -> dict:
    if session_id in sessions:
        sessions[session_id]["status"] = "ended"
        sessions[session_id]["end_time"] = datetime.utcnow().isoformat()
        return sessions[session_id]
    return { "error": "Session not found" }
