from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from bson import ObjectId

from app.services.model_service import model_service
from app.database import (
    users_collection,
    crop_history_collection
)


router = APIRouter(
    prefix="/crop",
    tags=["Crop Recommendation"]
)


# =====================================
# INPUT MODEL
# =====================================

class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float


# =====================================
# USER CROP INPUT
# Used for saving history
# =====================================

class UserCropInput(CropInput):
    user_id: str


# =====================================
# CROP RECOMMENDATION API
# =====================================

@router.post("/recommend")
def recommend_crop(data: CropInput):

    recommendations = model_service.recommend_crops(
        N=data.N,
        P=data.P,
        K=data.K,
        temperature=data.temperature,
        humidity=data.humidity,
        ph=data.ph,
        rainfall=data.rainfall
    )

    return {
        "recommendations": recommendations
    }


# =====================================
# CROP + MARKET ANALYSIS API
# WITH DATABASE HISTORY
# =====================================

@router.post("/recommend-with-market")
def recommend_with_market(data: UserCropInput):

    # ---------------------------------
    # VALIDATE USER ID
    # ---------------------------------

    try:
        object_id = ObjectId(data.user_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID."
        )

    # Check whether user exists
    user = users_collection.find_one(
        {"_id": object_id}
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    # ---------------------------------
    # STEP 1: CROP RECOMMENDATION
    # ---------------------------------

    recommendations = model_service.recommend_crops(
        N=data.N,
        P=data.P,
        K=data.K,
        temperature=data.temperature,
        humidity=data.humidity,
        ph=data.ph,
        rainfall=data.rainfall
    )

    # ---------------------------------
    # STEP 2: MARKET ANALYSIS
    # ---------------------------------

    market_analysis = model_service.analyze_market(
        recommendations
    )

    # ---------------------------------
    # STEP 3: FIND BEST CROP
    # ---------------------------------

    best_overall_crop = None

    if market_analysis:
        best_overall_crop = market_analysis[0]["crop"]

    # ---------------------------------
    # STEP 4: SAVE HISTORY TO MONGODB
    # ---------------------------------

    history_data = {
        "user_id": object_id,

        "input": {
            "N": data.N,
            "P": data.P,
            "K": data.K,
            "temperature": data.temperature,
            "humidity": data.humidity,
            "ph": data.ph,
            "rainfall": data.rainfall
        },

        "recommendations": recommendations,

        "market_analysis": market_analysis,

        "best_overall_crop": best_overall_crop,

        "created_at": datetime.now()
    }

    result = crop_history_collection.insert_one(
        history_data
    )

    # ---------------------------------
    # STEP 5: RETURN RESULT
    # ---------------------------------

    return {
        "message": (
            "Crop recommendation and market analysis "
            "completed and saved successfully!"
        ),

        "history_id": str(result.inserted_id),

        "recommendations": recommendations,

        "market_analysis": market_analysis,

        "best_overall_crop": best_overall_crop
    }


# =====================================
# TEST API
# =====================================

@router.get("/test")
def test_crop():

    return {
        "message": "Crop recommendation API is working!"
    }
# =====================================
# GET CROP RECOMMENDATION HISTORY
# =====================================

@router.get("/history/{user_id}")
def get_crop_history(user_id: str):

    # Validate user ID
    try:
        object_id = ObjectId(user_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID."
        )

    # Check user exists
    user = users_collection.find_one(
        {"_id": object_id}
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    # Get crop history
    history = list(
        crop_history_collection
        .find({"user_id": object_id})
        .sort("created_at", -1)
    )

    # Convert MongoDB ObjectId to string
    for item in history:
        item["_id"] = str(item["_id"])
        item["user_id"] = str(item["user_id"])

    return {
        "user_id": user_id,
        "total_recommendations": len(history),
        "history": history
    }