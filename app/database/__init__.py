import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_SVR = os.environ.get("MONGO_SVR","mongo")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")


client = pymongo.MongoClient(f"{MONGO_SVR}://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.6n6g3.mongodb.net/?retryWrites=true&w=majority")

db = client.WikiAPI

wikis_coll = db.wikis

users_coll = db.users
users_coll.create_index([('username', pymongo.ASCENDING)], unique=True)
