from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from ..database import SessionLocal
from ..models import User
import os, json

router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 2
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str

def create_access_token(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def log_login_event(username: str, role: str):
    entry = {
        "user_id": username,
        "event": "login_success",
        "role": role,
        "timestamp": datetime.utcnow().isoformat()
    }
    log_path = os.path.join("data", "audit_event_schema.json")
    try:
        if not os.path.exists(log_path):
            with open(log_path, "w") as f:
                json.dump([entry], f, indent=2)
        else:
            with open(log_path, "r+") as f:
                logs = json.load(f)
                logs.append(entry)
                f.seek(0)
                json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"[Audit] Failed to log login event: {e}")

@router.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == data.username).first()
        if not user or not pwd_context.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(user.username, user.role)
        log_login_event(user.username, user.role)

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": user.role
        }
    finally:
        db.close()