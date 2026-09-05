import joblib
import pandas as pd
from pathlib import Path


# Get the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to the saved ML model
MODEL_PATH = BASE_DIR / "models" / "crop_recommendation_model.pkl"


# Load the trained model
model = joblib.load(MODEL_PATH)


def predict_crop(N, P, K, temperature, humidity, ph, rainfall):
    """
    Predict the most suitable crop based on
    soil nutrients and weather conditions.
    """

    # Create input data with correct feature names
    input_data = pd.DataFrame(
        [[N, P, K, temperature, humidity, ph, rainfall]],
        columns=[
            "N",
            "P",
            "K",
            "temperature",
            "humidity",
            "ph",
            "rainfall"
        ]
    )

    # Make prediction
    prediction = model.predict(input_data)[0]

    return prediction


if __name__ == "__main__":

    result = predict_crop(
        N=90,
        P=42,
        K=43,
        temperature=20.8,
        humidity=82.0,
        ph=6.5,
        rainfall=200.0
    )

    print("Recommended Crop:", result)