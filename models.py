from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(
        String, unique=True, index=True, nullable=True
    )  # Optional for OAuth users
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    provider = Column(String, default="local")  # local, google, microsoft
    profile_picture = Column(String, nullable=True)
    role = Column(String, default="user")
