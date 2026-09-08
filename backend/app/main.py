from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routers import disease, crop, market, user


# =====================================
# CREATE FASTAPI APP
# =====================================

app = FastAPI(
    title="AgriVoice API",
    description="AI-powered agriculture assistance system",
    version="1.0.0"
)


# =====================================
# CORS CONFIGURATION
# =====================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://agrivoice-frontend.onrender.com",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =====================================
# UPLOAD DIRECTORY
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =====================================
# SERVE UPLOADED FILES
# =====================================

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads"
)


# =====================================
# INCLUDE ROUTERS
# =====================================

app.include_router(user.router)

app.include_router(crop.router)

app.include_router(disease.router)

app.include_router(market.router)


# =====================================
# ROOT API
# =====================================

@app.get("/")
def root():

    return {
        "message": "Welcome to AgriVoice API",
        "status": "running"
    }


# =====================================
# HEALTH CHECK
# =====================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }