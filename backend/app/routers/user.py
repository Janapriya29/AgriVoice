from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
import hashlib

from app.database import users_collection


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# =====================================
# USER REGISTRATION INPUT
# =====================================

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


# =====================================
# USER LOGIN INPUT
# =====================================

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# =====================================
# REGISTER USER
# =====================================

@router.post("/register")
def register_user(user: UserRegister):

    # Check whether email already exists
    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    # Hash password
    hashed_password = hashlib.sha256(
        user.password.encode()
    ).hexdigest()

    # Create user document
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.now()
    }

    # Save user in MongoDB
    result = users_collection.insert_one(
        new_user
    )

    return {
        "message": "User registered successfully!",
        "user_id": str(result.inserted_id),
        "name": user.name,
        "email": user.email
    }


# =====================================
# USER LOGIN
# =====================================

@router.post("/login")
def login_user(user: UserLogin):

    # Find user by email
    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    # Check whether user exists
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    # Hash entered password
    hashed_password = hashlib.sha256(
        user.password.encode()
    ).hexdigest()

    # Verify password
    if existing_user["password"] != hashed_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    # Login successful
    return {
        "message": "Login successful!",
        "user_id": str(existing_user["_id"]),
        "name": existing_user["name"],
        "email": existing_user["email"]
    }