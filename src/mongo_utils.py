import os
from pymongo import MongoClient
from dotenv import load_dotenv; load_dotenv()

# Loading environment variables
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

class MongoUtils():
    def __init__(self, db):
        client = MongoClient(CONNECTION_STRING)
        self.db = client[db]

    def push(self, coll, doc):
        self.db[coll].insert_one(doc)

    def fetch_applicant(self, coll, query):
        return self.db[coll].find_one(query)

    def get_count(self, coll):
        return self.db.coll.count_documents({})

    def get_recent(self, coll):
        '''Fetches last added record from the collection'''
        records = list(self.db[coll].find().sort("_id", -1).limit(1))
        return records[0]