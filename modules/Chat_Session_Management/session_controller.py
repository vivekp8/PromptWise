from modules.database import SessionLocal, Session
import uuid


def create_session(user_id: str) -> str:
    db = SessionLocal()
    session_id = str(uuid.uuid4())
    new_session = Session(session_id=session_id, user_id=user_id, active=True)
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
        }
    return None


def end_session(session_id: str) -> bool:
    db = SessionLocal()
    session = db.query(Session).filter(Session.session_id == session_id).first()
    if session and session.active:
        session.active = False
        db.commit()
        db.close()
        return True
    db.close()
    return False
