from fastapi import APIRouter
from pydantic import BaseModel

from app.services.model_service import model_service


router = APIRouter(
    prefix="/market",
    tags=["Market Analysis"]
)


class RecommendationItem(BaseModel):
    crop: str
    confidence: float


class MarketRequest(BaseModel):
    recommendations: list[RecommendationItem]


@router.post("/analyze")
def analyze_market(data: MarketRequest):

    recommendations = [
        {
            "crop": item.crop,
            "confidence": item.confidence
        }
        for item in data.recommendations
    ]

    results = model_service.analyze_market(
        recommendations
    )

    if not results:
        return {
            "message": "No market data available for the recommended crops.",
            "analysis": []
        }

    return {
        "message": "Market analysis completed successfully!",
        "analysis": results,
        "best_overall_crop": results[0]["crop"]
    }


@router.get("/test")
def test_market():
    return {
        "message": "Market analysis API is working!"
    }