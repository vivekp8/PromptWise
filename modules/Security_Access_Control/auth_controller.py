from sqlalchemy.orm import Session
from modules.database import SessionLocal, User # Consolidated Import
from passlib.context import CryptContext
from fastapi import HTTPException
from pydantic import BaseModel
import secrets # For reset tokens

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    username: str = None
    email: str = None
    password: str

class ProfileUpdate(BaseModel):
    user_id: int
    full_name: str
    email: str
    password: str = None

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

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
        provider="local"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return {"message": "User registered successfully", "user_id": new_user.id}

def authenticate_user(login: UserLogin):
    db = SessionLocal()
    user = None
    # Try username first, then email
    if login.username:
        user = db.query(User).filter(User.username == login.username).first()
    if not user and login.email:
        user = db.query(User).filter(User.email == login.email).first()
    db.close()
    
    if not user or not user.hashed_password:
        return None
    
    if not pwd_context.verify(login.password, user.hashed_password):
        return None
        
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
    return {"message": "Profile updated", "user": {"email": user.email, "full_name": user.full_name}}

def request_password_reset(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        db.close()
        # Mocking success to prevent email enumeration
        return {"message": "If this email exists, a reset link has been sent."}
    
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    db.commit()
    db.close()
    
    # Simulate sending email
    print(f"DEBUG: Password reset token for {email}: {token}")
    return {"message": "If this email exists, a reset link has been sent.", "debug_token": token}

def reset_password_with_token(data: ResetPasswordRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.reset_token == data.token).first()
    if not user:
        db.close()
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    user.hashed_password = pwd_context.hash(data.new_password)
    user.reset_token = None
    db.commit()
    db.close()
    return {"message": "Password reset successful"}

def mock_oauth_login(provider: str, email: str, name: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        user = User(
            email=email,
            full_name=name,
            provider=provider,
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    db.close()
    return user
