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

    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    hashed_password = hashlib.sha256(
        user.password.encode()
    ).hexdigest()

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.now()
    }

    result = users_collection.insert_one(new_user)

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

    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    hashed_password = hashlib.sha256(
        user.password.encode()
    ).hexdigest()

    if existing_user["password"] != hashed_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    return {
        "message": "Login successful!",
        "user_id": str(existing_user["_id"]),
        "name": existing_user["name"],
        "email": existing_user["email"]
    }