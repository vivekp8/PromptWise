from sqlalchemy import create_engine, Text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime
import os

# ✅ Database setup
DB_URL_ENV = os.getenv("DB_URL")
if DB_URL_ENV:
    DATABASE_URL = DB_URL_ENV
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.dirname(BASE_DIR)
    DB_PATH = os.path.join(ROOT_DIR, "promptwise.db")
    DATABASE_URL = f"sqlite:///{DB_PATH}"

# ✅ SQLAlchemy setup
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass


from sqlalchemy.orm import Mapped, mapped_column

# ✅ User model
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    username: Mapped[str | None] = mapped_column(unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column()
    hashed_password: Mapped[str | None] = mapped_column()
    provider: Mapped[str] = mapped_column(default="local")
    profile_picture: Mapped[str | None] = mapped_column()
    role: Mapped[str] = mapped_column(default="user")
    reset_token: Mapped[str | None] = mapped_column()  # Added for Forgot Password


# ✅ Session model
class Session(Base):
    __tablename__ = "sessions"
    session_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)
    title: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# ✅ Chat Message model
class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(index=True) # ForeignKey could be added but keeping simple for now
    role: Mapped[str] = mapped_column() # "user" or "assistant"
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# ✅ Feedback model with timestamp
class Feedback(Base):
    __tablename__ = "feedback"
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    prompt: Mapped[str] = mapped_column(Text)
    label: Mapped[str] = mapped_column()
    feedback: Mapped[str] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# ✅ Create tables on startup
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
else:
    init_db()
