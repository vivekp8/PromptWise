from modules.database import SessionLocal, Session
import uuid


def create_session(user_id: str, title: str = "New Chat") -> str:
    db = SessionLocal()
    session_id = str(uuid.uuid4())
    new_session = Session(session_id=session_id, user_id=user_id, active=True, title=title)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    db.close()
    return session_id


def get_session(session_id: str) -> dict:
    db = SessionLocal()
    session = db.query(Session).filter(Session.session_id == session_id).first()
    db.close()
    if session:
        return {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "active": session.active,
            "title": session.title
        }
    return None


def update_session_title(session_id: str, title: str) -> bool:
    db = SessionLocal()
    session = db.query(Session).filter(Session.session_id == session_id).first()
    if session:
        session.title = title
        db.commit()
        db.close()
        return True
    db.close()
    return False


def delete_session(session_id: str) -> bool:
    db = SessionLocal()
    session = db.query(Session).filter(Session.session_id == session_id).first()
    if session:
        session.active = False # Soft delete
        db.commit()
        db.close()
        return True
    db.close()
    return False


def get_user_sessions(user_id: str):
    db = SessionLocal()
    sessions = db.query(Session).filter(Session.user_id == user_id, Session.active == True).order_by(Session.created_at.desc()).all()
    db.close()
    return [{"session_id": s.session_id, "created_at": s.created_at, "title": s.title or "New Chat"} for s in sessions]


from modules.database import Message

def add_message(session_id: str, role: str, content: str):
    db = SessionLocal()
    msg = Message(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    db.close()
    return msg

def get_chat_history(session_id: str):
    db = SessionLocal()
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp).all()
    db.close()
    return [{"role": m.role, "content": m.content} for m in messages]
