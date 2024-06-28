from pymongo import MongoClient
from pymongo.errors import PyMongoError

class Mongo_Config:
    HOST = "mongo"
    PORT = 27017
    DB = "records"
    
    RECORDS_COLLECTION = "records"
    USERS_COLLECTION = "users"

    # Get the relevant collections
    client = MongoClient(host=HOST, port=PORT)
    db = client[DB]

    records = db[RECORDS_COLLECTION]
    users = db[USERS_COLLECTION]