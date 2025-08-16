from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PromptWise.models import Base

SQLALCHEMY_DB_URL = "sqlite:///PromptWise/data/users.db"

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Initialize database and tables
Base.metadata.create_all(bind=engine)