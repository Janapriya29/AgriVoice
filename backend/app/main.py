from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import disease, crop, market, user

app = FastAPI(
    title="AgriVoice API"
)

# Allow React frontend to communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded disease images
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# Include API routers
app.include_router(user.router)
app.include_router(disease.router)
app.include_router(crop.router)
app.include_router(market.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to AgriVoice API"
    }