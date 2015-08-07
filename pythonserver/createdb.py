from pymongo import MongoClient
import pymongo

if __name__ == "__main__":
    client = MongoClient()
    db = client.bonusprocessing
    cardscollection = db.cards
    cardscollection.create_index([("code", pymongo.ASCENDING)], unique=True)