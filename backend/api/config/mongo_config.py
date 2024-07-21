from pymongo import MongoClient

class Mongo_Config:
    client = MongoClient(host='mongo', port=27017)
    db = client['records']

    submissions = db['submissions']
    namechanges = db['namechanges']

    accounts = db['accounts']
    audit_log = db['audit_log']

    leaderboard = db['leaderboard']
    oauth = db['oauth']
