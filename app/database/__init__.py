import pymongo

MONGO_SVR = "mongodb+srv"
USER = "admin"
PASSWORD = "1234abcd"
DB = "test"


client = pymongo.MongoClient(f"{MONGO_SVR}://{USER}:{PASSWORD}@cluster0.6n6g3.mongodb.net/?retryWrites=true&w=majority")

db = client.WikiAPI

wikis_coll = db.wikis

users_coll = db.users
users_coll.create_index([('username', pymongo.ASCENDING)], unique=True)
