from sqlalchemy import create_engine, Column, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ Correct relative path to your database file
DATABASE_URL = "sqlite:///../database/promptwise.db"

# ✅ Create engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


# ✅ Session table
class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(String)
    active = Column(Boolean, default=True)


# ✅ Feedback table
class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(String, primary_key=True, index=True)
    prompt = Column(Text)
    label = Column(String)
    feedback = Column(String)


# ✅ Create tables in the database
Base.metadata.create_all(bind=engine)
