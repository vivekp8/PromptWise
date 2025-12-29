from sqlalchemy.orm import Session as DBSession
from modules.database import Session, SessionLocal


def create_session(user_id: str) -> str:
    db: DBSession = SessionLocal()
    session_id = f"{user_id}_session"

    # Check if session already exists
    existing = db.query(Session).filter(Session.session_id == session_id).first()
    if not existing:
        new_session = Session(session_id=session_id, user_id=user_id, active=True)
        db.add(new_session)
        db.commit()
    db.close()
    return session_id


def get_session(session_id: str):
    db: DBSession = SessionLocal()
    session = db.query(Session).filter(Session.session_id == session_id).first()
    db.close()
    if session:
        return {"user_id": session.user_id, "active": session.active}
    return None
