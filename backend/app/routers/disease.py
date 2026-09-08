from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from PIL import Image
from datetime import datetime
from pathlib import Path
from bson import ObjectId
import io
import uuid

from app.services.model_service import model_service
from app.database import (
    users_collection,
    disease_history_collection
)


router = APIRouter(
    prefix="/disease",
    tags=["Disease Prediction"]
)


# =====================================
# UPLOAD FOLDER
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

UPLOAD_DIR = (
    BASE_DIR
    / "uploads"
    / "disease_images"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =====================================
# DISEASE PREDICTION API
# =====================================

@router.post("/predict")
async def predict_disease(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):

    # ---------------------------------
    # VALIDATE USER ID
    # ---------------------------------

    try:
        object_id = ObjectId(user_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID."
        )

    user = users_collection.find_one(
        {"_id": object_id}
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    # ---------------------------------
    # VALIDATE IMAGE
    # ---------------------------------

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image file."
        )

    try:

        # Read uploaded image
        image_bytes = await file.read()

        # Open uploaded image
        image = Image.open(
            io.BytesIO(image_bytes)
        )

        # ---------------------------------
        # CREATE UNIQUE IMAGE NAME
        # ---------------------------------

        file_extension = Path(
            file.filename
        ).suffix

        unique_filename = (
            f"{uuid.uuid4()}"
            f"{file_extension}"
        )

        image_path = (
            UPLOAD_DIR
            / unique_filename
        )

        # ---------------------------------
        # SAVE IMAGE
        # ---------------------------------

        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)

        # ---------------------------------
        # GET ML PREDICTION
        # ---------------------------------

        prediction_result = (
            model_service.predict_disease(image)
        )

        # ---------------------------------
        # IMAGE URL
        # ---------------------------------

        image_url = (
            f"/uploads/disease_images/"
            f"{unique_filename}"
        )

        # ---------------------------------
        # SAVE TO MONGODB
        # ---------------------------------

        history_data = {
            "user_id": object_id,

            "prediction": prediction_result[
                "prediction"
            ],

            "confidence": prediction_result[
                "confidence"
            ],

            "image_url": image_url,

            "created_at": datetime.now()
        }

        result = disease_history_collection.insert_one(
            history_data
        )

        # ---------------------------------
        # RETURN RESULT
        # ---------------------------------

        return {
            "message": (
                "Disease prediction completed "
                "and saved successfully!"
            ),

            "history_id": str(result.inserted_id),

            "prediction": prediction_result[
                "prediction"
            ],

            "confidence": prediction_result[
                "confidence"
            ],

            "image_url": image_url
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )


# =====================================
# GET DISEASE PREDICTION HISTORY
# =====================================

@router.get("/history/{user_id}")
def get_disease_history(user_id: str):

    # ---------------------------------
    # VALIDATE USER ID
    # ---------------------------------

    try:
        object_id = ObjectId(user_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID."
        )

    # ---------------------------------
    # CHECK USER EXISTS
    # ---------------------------------

    user = users_collection.find_one(
        {"_id": object_id}
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    # ---------------------------------
    # GET PREDICTION HISTORY
    # ---------------------------------

    history = list(
        disease_history_collection
        .find({"user_id": object_id})
        .sort("created_at", -1)
    )

    # ---------------------------------
    # CONVERT MONGODB DATA TO JSON
    # ---------------------------------

    for item in history:

        item["_id"] = str(item["_id"])
        item["user_id"] = str(item["user_id"])

        # ---------------------------------
        # ADD FULL RENDER URL FOR FRONTEND
        # ---------------------------------

        if "image_url" in item:
            item["image_url"] = (
                "https://agrivoice-e14c.onrender.com"
                + item["image_url"]
            )

    # ---------------------------------
    # RETURN HISTORY
    # ---------------------------------

    return {
        "user_id": user_id,
        "total_predictions": len(history),
        "history": history
    }


# =====================================
# TEST API
# =====================================

@router.get("/test")
def test_disease():

    return {
        "message": "Disease prediction API is working!"
    }