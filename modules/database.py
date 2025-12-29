from sqlalchemy import create_engine, Column, String, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

import os

# ✅ SQLite database path - Using absolute path to avoid CWD issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level from 'modules' to root, then point to 'promptwise.db'
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(ROOT_DIR, "promptwise.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# ✅ SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


# ✅ Session model
class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(String)
    active = Column(Boolean, default=True)


# ✅ Feedback model with timestamp
class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(String, primary_key=True, index=True)
    prompt = Column(Text)
    label = Column(String)
    feedback = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)  # ✅ Added timestamp


# ✅ Create tables
Base.metadata.create_all(bind=engine)
