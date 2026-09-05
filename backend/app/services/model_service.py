import joblib
import numpy as np
import tensorflow as tf

from app.config import (
    DISEASE_MODEL_PATH,
    CROP_MODEL_PATH,
    SCALER_PATH,
    LABEL_ENCODER_PATH,
    FEATURE_PATH,
    MARKET_DATA_PATH
)


class ModelService:

    def __init__(self):

        print("Loading AgriVoice models...")

        # =====================================
        # LOAD DISEASE PREDICTION MODEL
        # =====================================
        self.disease_model = tf.keras.models.load_model(
            DISEASE_MODEL_PATH
        )

        # Exact class order used during training
        self.disease_classes = [
            "Pepper,_bell___Bacterial_spot",
            "Pepper,_bell___healthy",
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy",
            "Tomato___Bacterial_spot",
            "Tomato___Early_blight",
            "Tomato___Late_blight",
            "Tomato___healthy"
        ]

        # =====================================
        # LOAD CROP RECOMMENDATION MODEL
        # =====================================
        self.crop_model = joblib.load(
            CROP_MODEL_PATH
        )

        self.scaler = joblib.load(
            SCALER_PATH
        )

        self.label_encoder = joblib.load(
            LABEL_ENCODER_PATH
        )

        self.features = joblib.load(
            FEATURE_PATH
        )

        # =====================================
        # LOAD MARKET PRICE DATA
        # =====================================
        self.market_prices = joblib.load(
            MARKET_DATA_PATH
        )

        print("All models loaded successfully!")

    # =====================================
    # PLANT DISEASE PREDICTION
    # =====================================

    def predict_disease(self, image):

        # Convert image to RGB
        image = image.convert("RGB")

        # Resize image to model input size
        image = image.resize((224, 224))

        # Convert to NumPy array
        image_array = np.array(image)

        # Convert to float
        image_array = image_array.astype(
            "float32"
        )

        # Add batch dimension
        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        # Get model prediction
        predictions = self.disease_model.predict(
            image_array,
            verbose=0
        )

        # Get highest prediction
        predicted_index = int(
            np.argmax(predictions[0])
        )

        confidence = float(
            predictions[0][predicted_index] * 100
        )

        predicted_class = self.disease_classes[
            predicted_index
        ]

        # Convert technical class name
        # into readable text
        readable_name = (
            predicted_class
            .replace("___", " - ")
            .replace("_", " ")
            .replace(",", "")
        )

        return {
            "prediction": readable_name,
            "confidence": round(confidence, 2)
        }

    # =====================================
    # CROP RECOMMENDATION
    # =====================================

    def recommend_crops(
        self,
        N,
        P,
        K,
        temperature,
        humidity,
        ph,
        rainfall
    ):

        input_data = np.array([
            [
                N,
                P,
                K,
                temperature,
                humidity,
                ph,
                rainfall
            ]
        ])

        scaled_data = self.scaler.transform(
            input_data
        )

        probabilities = self.crop_model.predict_proba(
            scaled_data
        )[0]

        top_indices = np.argsort(
            probabilities
        )[-3:][::-1]

        recommendations = []

        for index in top_indices:

            crop = self.label_encoder.inverse_transform(
                [index]
            )[0]

            confidence = float(
                probabilities[index] * 100
            )

            recommendations.append({
                "crop": crop,
                "confidence": round(confidence, 2)
            })

        return recommendations

    # =====================================
    # MARKET ANALYSIS
    # =====================================

    def analyze_market(self, recommendations):

        results = []

        max_market_price = max(
            float(data["modal_price"])
            for data in self.market_prices.values()
        )

        for item in recommendations:

            crop = item["crop"].lower().strip()
            confidence = float(item["confidence"])

            # Skip crops without market data
            if crop not in self.market_prices:
                continue

            price_info = self.market_prices[crop]

            modal_price = float(
                price_info["modal_price"]
            )

            markets_available = int(
                price_info["markets"]
            )

            price_score = (
                modal_price / max_market_price
            ) * 100

            combined_score = (
                0.70 * confidence
                + 0.30 * price_score
            )

            estimated_cost = (
                modal_price * 0.60
            )

            estimated_profit = (
                modal_price - estimated_cost
            )

            results.append({
                "crop": crop,
                "ml_confidence": round(confidence, 2),
                "average_modal_price": round(
                    modal_price, 2
                ),
                "markets_available": markets_available,
                "price_score": round(
                    price_score, 2
                ),
                "combined_score": round(
                    combined_score, 2
                ),
                "estimated_cost": round(
                    estimated_cost, 2
                ),
                "estimated_profit": round(
                    estimated_profit, 2
                )
            })

        results.sort(
            key=lambda x: x["combined_score"],
            reverse=True
        )

        return results


# =====================================
# SHARED MODEL SERVICE
# =====================================

model_service = ModelService()