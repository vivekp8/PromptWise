from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from modules.Chat_Session_Management import session_controller
from modules.Prompt_Engine import ml_classifier, feedback_logger
from modules.database import Feedback, SessionLocal, User, engine, init_db # Consolidated
from modules.Security_Access_Control import auth_controller
from modules.Prompt_Engine.vector_store import vector_store
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize DB Tables
init_db()

app = FastAPI()

# ✅ CORS setup
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Request models
class PromptRequest(BaseModel):
    prompt: str


class FeedbackRequest(BaseModel):
    prompt: str
    feedback: str


class SessionRequest(BaseModel):
    user_id: str
    title: str = "New Chat"

class RenameSessionRequest(BaseModel):
    title: str

# ✅ Response models
class ClassifyResponse(BaseModel):
    label: str
    response: str


class FeedbackResponse(BaseModel):
    status: str
    label: str


class SessionResponse(BaseModel):
    session_id: str

class SessionInfo(BaseModel):
    session_id: str
    user_id: str
    active: bool
    title: str

class SessionDataResponse(BaseModel):
    session: SessionInfo | str

@app.post("/session/create", response_model=SessionResponse)
def create_session(req: SessionRequest):
    session_id = session_controller.create_session(req.user_id, req.title)
    return SessionResponse(session_id=session_id)

@app.patch("/session/{session_id}/title")
def rename_session(session_id: str, req: RenameSessionRequest):
    success = session_controller.update_session_title(session_id, req.title)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "success", "title": req.title}

@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    success = session_controller.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "success", "message": "Session deleted"}


@app.get("/session/{session_id}", response_model=SessionDataResponse)
def get_session(session_id: str):
    session = session_controller.get_session(session_id)
    return SessionDataResponse(session=session or "not found")


# ✅ NEW: Chat Endpoints
class ChatMessageRequest(BaseModel):
    session_id: str
    message: str
    model: str = "gpt-3.5-turbo"

class ChatHistoryResponse(BaseModel):
    history: list[dict]

@app.post("/chat/message")
def send_chat_message(req: ChatMessageRequest):
    # 1. Save User Message
    print(f"DEBUG: Received chat request. Model: {req.model}, Message: {req.message[:50]}...")
    session_controller.add_message(req.session_id, "user", req.message)
    
    # 2. Retrieve History
    history = session_controller.get_chat_history(req.session_id)
    
    # 3. Check for RAG context (simplified)
    # We can check if the last message (req.message) is a question
    # This logic can be more sophisticated (using ml_classifier classification)
    
    # For now, let's just pass raw text to LLM since LLMClient handles it
    # But if we want RAG, we should do it here before calling LLM.
    
    context_text = ""
    # Optional: Retrieve RAG context if it looks like a question
    if "?" in req.message:
        docs = vector_store.search(req.message)
        if docs:
             context_text = "\nContext:\n" + "\n".join(docs)

    system_prompt = "You are PromptWise Copilot, a helpful AI assistant."
    if context_text:
        system_prompt += f"\n{context_text}"
        
    # 4. Generate Response
    # We pass history (excluding the very last one we just added if we want stricter control, 
    # but llm_client logic expects history to be previous messages. 
    # Actually, verify_llm logic:
    # OpenAI: we pass all messages.
    # Google: we pass history to start_chat, then send active message.
    
    # Let's align: get_chat_history returns ALL messages including the one we just saved.
    # So for OpenAI we pass all.
    # For Gemini we might need to separate.
    
    # For simplicity, let's rely on LLMClient to handle `prompt` + `history`.
    # We will exclude the *current* prompt from history passed to LLMClient 
    # because LLMClient.generate_response takes (prompt, history).
    
    past_history = history[:-1] # All except the one we just added
    
    response_text = "I'm sorry, I couldn't generate a response."
    try:
        from LLM_Provider_Orchestration.llm_client import llm_client
        response_text = llm_client.generate_response(req.message, past_history, system_prompt, model_name=req.model)
    except Exception as e:
        response_text = f"Error: {str(e)}"
        
    # 5. Save Assistant Message
    session_controller.add_message(req.session_id, "assistant", response_text)
    
    return {"role": "assistant", "content": response_text}

@app.get("/chat/history/{session_id}", response_model=ChatHistoryResponse)
def get_history(session_id: str):
    history = session_controller.get_chat_history(session_id)
    return ChatHistoryResponse(history=history)


@app.get("/sessions/{user_id}")
def get_user_sessions(user_id: str):
    sessions = session_controller.get_user_sessions(user_id)
    return {"sessions": sessions}


# ✅ NEW: Feedback Dashboard Endpoint
@app.get("/feedback/all")
def get_all_feedback():
    db = SessionLocal()
    feedback_entries = db.query(Feedback).all()
    db.close()
    return {
        "feedback": [
            {
                "prompt": f.prompt,
                "label": f.label,
                "feedback": f.feedback,
                "timestamp": f.timestamp,
            }
            for f in feedback_entries
        ]
    }


# ✅ NEW: Analytics Endpoint
@app.get("/feedback/stats")
def get_feedback_stats():
    db = SessionLocal()
    feedback_entries = db.query(Feedback).all()
    db.close()

    label_counts = {}
    for entry in feedback_entries:
        label = entry.label or "unknown"
        label_counts[label] = label_counts.get(label, 0) + 1

    return {"label_distribution": label_counts, "total": len(feedback_entries)}


# ✅ NEW: Export Endpoint
from fastapi.responses import StreamingResponse
import csv
import io


@app.get("/feedback/export")
def export_feedback():
    db = SessionLocal()
    feedback_entries = db.query(Feedback).all()
    db.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Prompt", "Label", "Feedback", "Timestamp"])

    for entry in feedback_entries:
        writer.writerow(
            [entry.id, entry.prompt, entry.label, entry.feedback, entry.timestamp]
        )

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=feedback_export.csv"},
    )


# ✅ AUTHENTICATION ROUTES


from utils.jwt_utils import create_access_token, get_current_user
import json

# ... (existing imports)

# ... (existing code)

# ✅ AUTHENTICATION ROUTES

@app.post("/auth/register")
def register(user: auth_controller.UserRegister):
    result = auth_controller.register_user(user)
    
    # ✅ Log Audit Event
    try:
        from modules.Security_Access_Control.audit_logger import log_event
        log_event(event="USER_REGISTER", user_email=user.email, role="user", details={"name": user.full_name})
    except Exception as e:
        print(f"Audit Log Error: {e}")
        
    return result


@app.post("/auth/login")
def login(creds: auth_controller.UserLogin):
    user = auth_controller.authenticate_user(creds)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate Token
    token = create_access_token({"sub": user.email, "role": user.role})
    
    # ✅ Log Audit Event
    try:
        from modules.Security_Access_Control.audit_logger import log_event
        log_event(event="USER_LOGIN", user_email=user.email, role=user.role, details={"method": "password"})
    except Exception as e:
        print(f"Audit Log Error: {e}")

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "user": {"id": user.id, "email": user.email, "username": user.username, "full_name": user.full_name},
    }

AUDIT_LOG_PATH = os.path.join("data", "audit_event_schema.json")

@app.get("/admin/audit/events")
def get_audit_events(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["superadmin", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    try:
        if os.path.exists(AUDIT_LOG_PATH):
            with open(AUDIT_LOG_PATH, "r") as f:
                logs = json.load(f)
            return {"events": logs}
        else:
            return {"events": []}
    except Exception as e:
        print(f"Error reading audit logs: {e}")
        return {"events": []}


# ✅ ADMIN PANEL ENDPOINTS

@app.get("/admin/stats")
def get_admin_stats(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["superadmin", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    db = SessionLocal()
    try:
        from modules.database import User, Session as DBSession, Message, Feedback
        total_users = db.query(User).count()
        active_sessions = db.query(DBSession).filter(DBSession.active == True).count()
        total_prompts = db.query(Message).count()
        total_feedback = db.query(Feedback).count()
        return {
            "total_users": total_users,
            "active_sessions": active_sessions,
            "total_prompts": total_prompts,
            "total_feedback": total_feedback,
        }
    finally:
        db.close()


@app.get("/admin/users")
def get_admin_users(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["superadmin", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return {
            "users": [
                {
                    "id": u.id,
                    "email": u.email,
                    "username": u.username,
                    "full_name": u.full_name,
                    "role": u.role,
                    "provider": u.provider,
                }
                for u in users
            ]
        }
    finally:
        db.close()


@app.delete("/admin/users/{user_id}")
def delete_admin_user(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmin can delete users")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # Prevent self-deletion
        if user.email == current_user["sub"]:
            raise HTTPException(status_code=400, detail="Cannot delete your own account")
        db.delete(user)
        db.commit()
        return {"message": f"User {user.email} deleted successfully"}
    finally:
        db.close()


class RoleUpdateRequest(BaseModel):
    role: str


@app.put("/admin/users/{user_id}/role")
def update_user_role(user_id: int, req: RoleUpdateRequest, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmin can change user roles")
    if req.role not in ["user", "admin", "superadmin", "auditor"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.role = req.role
        db.commit()
        return {"message": f"Role updated to {req.role}", "user_id": user_id}
    finally:
        db.close()


@app.put("/auth/profile")
def update_profile(data: auth_controller.ProfileUpdate):
    return auth_controller.update_user_profile(data)


@app.post("/auth/forgot-password")
def forgot_password(data: auth_controller.ForgotPasswordRequest):
    return auth_controller.request_password_reset(data.email)


@app.post("/auth/reset-password")
def reset_password(data: auth_controller.ResetPasswordRequest):
    return auth_controller.reset_password_with_token(data)


class OAuthRequest(BaseModel):
    provider: str  # google, microsoft
    email: str
    name: str


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        # Seed or Update Default Superadmin
        admin_username = "vivekp#8"
        existing_admin = db.query(User).filter(User.username == admin_username).first()

        hashed_pw = auth_controller.pwd_context.hash("vivekp8#pwa")

        if not existing_admin:
            print(f"[SEED] Seeding superadmin user: {admin_username}")
            admin_user = User(
                email="vivekpotnuru8@gmail.com",
                username=admin_username,
                full_name="Vivek Potnuru",
                hashed_password=hashed_pw,
                role="superadmin",
                provider="local",
            )
            db.add(admin_user)
            print("[OK] Superadmin user created successfully")
        else:
            print(f"[UPDATE] Updating superadmin: {admin_username}")
            existing_admin.hashed_password = hashed_pw
            existing_admin.role = "superadmin"
            print("[OK] Superadmin password and role updated")

        db.commit()
        # Seed Knowledge Base for RAG
        knowledge_docs = [
            "PromptWise is an advanced AI interface for prompt classification and session management.",
            "It supports RAG (Retrieval-Augmented Generation) to provide context-aware responses.",
            "Users can submit feedback to improve the model's performance over time.",
            "The system uses FastAPI for the backend and React for the frontend.",
            "Authentication is handled via JWT and supports Google/Microsoft OAuth (mocked)."
        ]
        try:
            print("[SEED] Indexing knowledge base...")
            vector_store.add_documents(knowledge_docs)
            print("[OK] Knowledge base indexed successfully")
        except Exception as e:
            print(f"[WARN] Knowledge base indexing failed (likely missing API Key): {e}")

    except Exception as e:
        print(f"[ERROR] Startup seeding failed: {e}")
        db.rollback()
    finally:
        db.close()


@app.post("/auth/oauth")
def oauth_login(data: OAuthRequest):
    try:
        # Simulated backend verification
        user = auth_controller.mock_oauth_login(data.provider, data.email, data.name)
        return {
            "message": "OAuth Login successful",
            "user": {"id": user.id, "email": user.email, "full_name": user.full_name},
        }
    except Exception as e:
        print(f"OAuth Error: {e}")
        # Return a more descriptive error if possible, or at least 500
        raise HTTPException(status_code=500, detail=f"OAuth login failed: {str(e)}")
