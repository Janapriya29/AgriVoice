from pathlib import Path

# Main AgriVoice project folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Models folder
MODEL_DIR = BASE_DIR / "models"

# Disease prediction model
DISEASE_MODEL_PATH = MODEL_DIR / "crop_disease_model.keras"

# Crop recommendation model
CROP_MODEL_PATH = MODEL_DIR / "crop_recommendation_model.pkl"

# Preprocessing files
SCALER_PATH = MODEL_DIR / "crop_scaler.pkl"
LABEL_ENCODER_PATH = MODEL_DIR / "crop_label_encoder.pkl"
FEATURE_PATH = MODEL_DIR / "crop_features.pkl"

# Market price data
MARKET_DATA_PATH = MODEL_DIR / "crop_market_prices.pkl"