from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("MONGO_DB", "mergington")


def get_client():
    return MongoClient(MONGO_URI)


def get_db():
    client = get_client()
    return client[DB_NAME]


def get_activities_collection():
    db = get_db()
    return db.activities
