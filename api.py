from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from modules.Chat_Session_Management import session_controller
from modules.Prompt_Engine import ml_classifier, feedback_logger
from modules.database import Feedback, SessionLocal, engine
from modules.Security_Access_Control import auth_controller
from models import Base, User

# ✅ Initialize DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],  # You can restrict this to ["http://localhost:5173"] later
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


# ✅ Response models
class ClassifyResponse(BaseModel):
    label: str
    response: str


class FeedbackResponse(BaseModel):
    status: str
    label: str


class SessionResponse(BaseModel):
    session_id: str


class SessionDataResponse(BaseModel):
    session: dict | str


# ✅ Endpoints
@app.post("/classify", response_model=ClassifyResponse)
def classify_prompt(req: PromptRequest):
    label = ml_classifier.classify_prompt(req.prompt)
    response = ml_classifier.route_prompt(req.prompt)
    return ClassifyResponse(label=label, response=response)


@app.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(req: FeedbackRequest):
    label = ml_classifier.classify_prompt(req.prompt)
    feedback_logger.log_feedback(req.prompt, label, req.feedback)
    return FeedbackResponse(status="logged", label=label)


@app.post("/session/create", response_model=SessionResponse)
def create_session(req: SessionRequest):
    session_id = session_controller.create_session(req.user_id)
    return SessionResponse(session_id=session_id)


@app.get("/session/{session_id}", response_model=SessionDataResponse)
def get_session(session_id: str):
    session = session_controller.get_session(session_id)
    return SessionDataResponse(session=session or "not found")


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


@app.post("/auth/register")
def register(user: auth_controller.UserRegister):
    return auth_controller.register_user(user)


@app.post("/auth/login")
def login(creds: auth_controller.UserLogin):
    user = auth_controller.authenticate_user(creds)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "message": "Login successful",
        "user": {"id": user.id, "email": user.email, "full_name": user.full_name},
    }


@app.put("/auth/profile")
def update_profile(data: auth_controller.ProfileUpdate):
    return auth_controller.update_user_profile(data)


class OAuthRequest(BaseModel):
    provider: str  # google, microsoft
    email: str
    name: str


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        # Seed or Update Admin User
        admin_email = "vivekpotnuru8@gmail.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()

        hashed_pw = auth_controller.pwd_context.hash("vivekp8#pw")

        if not existing_admin:
            print(f"🚀 Seeding admin user: {admin_email}")
            admin_user = User(
                email=admin_email,
                username="vivekp8",
                full_name="Vivek Potnuru",
                hashed_password=hashed_pw,
                role="superadmin",
                provider="local",
            )
            db.add(admin_user)
            print("✅ Admin user created successfully")
        else:
            print(f"🔄 Updating admin password for: {admin_email}")
            existing_admin.hashed_password = hashed_pw
            existing_admin.role = "superadmin"  # Ensure role is correct too
            print("✅ Admin password and role updated")

        db.commit()
    except Exception as e:
        print(f"❌ Startup seeding failed: {e}")
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
