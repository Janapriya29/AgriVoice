import os
from pymongo import MongoClient

# =====================================
# MONGODB CONNECTION
# =====================================

# Render will use the MONGODB_URL environment variable.
# If it is not available, local MongoDB will be used.
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://localhost:27017"
)

client = MongoClient(
    MONGODB_URL,
    serverSelectionTimeoutMS=10000
)

# =====================================
# TEST DATABASE CONNECTION
# =====================================

try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")
except Exception as e:
    print("MongoDB connection failed:", e)

# =====================================
# AGRIVOICE DATABASE
# =====================================

db = client["agrivoice"]

# =====================================
# DATABASE COLLECTIONS
# =====================================

users_collection = db["users"]

disease_history_collection = db["disease_history"]

crop_history_collection = db["crop_history"]