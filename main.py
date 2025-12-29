from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

# 🌐 Base directory and DB setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "PromptWise", "database", "promptwise.db")

# ✅ Ensure DB file and directory exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if not os.path.isfile(DB_PATH):
    open(DB_PATH, "a").close()

# 🚀 Initialize FastAPI
app = FastAPI(title="PromptWise API", version="1.0.0")

# 🔒 CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔐 Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Mount static assets (for favicons, etc.)
STATIC_DIR = os.path.join(BASE_DIR, "PromptWise", "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 🔗 Include module routers
from PromptWise.Prompt_Dashboard import prompt_routes
from PromptWise.Admin_Dashboard import (
    auth_routes,
    admin_routes,
    admin_export,
    audit_routes,
)

app.include_router(prompt_routes.router)
app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(admin_export.router)
app.include_router(audit_routes.router)


# ✅ Health check
@app.get("/")
def health_check():
    return {"status": "running", "app": "PromptWise Backend"}


# 🌟 Unified favicon route (supports light/dark mode)
@app.get("/favicon.ico", include_in_schema=False)
def serve_favicon(request: Request):
    # Check optional header sent from frontend
    prefers_dark = request.headers.get("X-DARK-MODE", "false") == "true"
    selected = "favicon-dark.ico" if prefers_dark else "favicon-light.ico"
    filepath = os.path.join(STATIC_DIR, selected)

    # Fall back if file is missing
    if not os.path.isfile(filepath):
        filepath = os.path.join(STATIC_DIR, "favicon.ico")  # optional fallback
    return FileResponse(filepath)
