from modules.database import SessionLocal, Feedback
import uuid
from datetime import datetime


def log_feedback(prompt: str, label: str, feedback: str):
    db = SessionLocal()
    new_entry = Feedback(
        id=str(uuid.uuid4()),
        prompt=prompt,
        label=label,
        feedback=feedback,
        timestamp=datetime.utcnow(),
    )
    db.add(new_entry)
    db.commit()
    db.close()
