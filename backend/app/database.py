from pymongo import MongoClient

# MongoDB connection URL
MONGODB_URL = "mongodb://localhost:27017"

# Create MongoDB client
client = MongoClient(MONGODB_URL)

# AgriVoice database
db = client["agrivoice"]


# =====================================
# DATABASE COLLECTIONS
# =====================================

users_collection = db["users"]

disease_history_collection = db["disease_history"]

crop_history_collection = db["crop_history"]