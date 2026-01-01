from pymongo import MongoClient
from api.core.config import MONGO_URI, MONGO_DB

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]