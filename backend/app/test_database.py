from app.database import db

try:

    # Test connection
    db.command("ping")

    print("MongoDB connected successfully!")
    print("Database name:", db.name)

except Exception as error:

    print("MongoDB connection failed!")
    print(error)