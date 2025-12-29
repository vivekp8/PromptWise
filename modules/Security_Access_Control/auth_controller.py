from sqlalchemy.orm import Session
from modules.database import SessionLocal
from models import User
from passlib.context import CryptContext
from fastapi import HTTPException
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: str
    password: str


class ProfileUpdate(BaseModel):
    user_id: int
    full_name: str
    email: str
    password: str = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def register_user(user: UserRegister):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_pw,
        full_name=user.full_name,
        provider="local",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return {"message": "User registered successfully", "user_id": new_user.id}


def authenticate_user(login: UserLogin):
    print(f"🕵️ DEBUG: Attempting login for email: '{login.email}'")
    db = SessionLocal()
    user = db.query(User).filter(User.email == login.email).first()
    db.close()

    if not user:
        print(f"❌ DEBUG: User NOT FOUND for email: '{login.email}'")
        return None

    print(
        f"✅ DEBUG: User found. ID: {user.id}, Role: {user.role}, Has Password: {bool(user.hashed_password)}"
    )

    if not user.hashed_password:
        print("❌ DEBUG: User has no password hash.")
        return None

    if not pwd_context.verify(login.password, user.hashed_password):
        print("❌ DEBUG: Password verification FAILED.")
        # print(f"   Input: '{login.password}'") # Be careful printing passwords, but for local debug it's unlikely to leak
        return None

    print("✅ DEBUG: Password verified successfully.")
    return user


def update_user_profile(update_data: ProfileUpdate):
    db = SessionLocal()
    user = db.query(User).filter(User.id == update_data.user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    user.full_name = update_data.full_name
    user.email = update_data.email
    if update_data.password:
        user.hashed_password = pwd_context.hash(update_data.password)

    db.commit()
    db.refresh(user)
    db.close()
    return {
        "message": "Profile updated",
        "user": {"email": user.email, "full_name": user.full_name},
    }


def mock_oauth_login(provider: str, email: str, name: str):
    print(f"🕵️ DEBUG: OAuth Login for {email} ({provider})")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            print("INFO: Creating new OAuth user")
            # Auto-register OAuth user
            user = User(email=email, full_name=name, provider=provider, role="user")
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✅ DEBUG: Created OAuth user {user.id}")
        else:
            print(f"✅ DEBUG: Found existing OAuth user {user.id}")

    except Exception as e:
        print(f"❌ DEBUG: Database error in OAuth: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

    return user
