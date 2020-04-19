from pymongo import MongoClient
from pymongo.database import Database


DB: Database = None


def connect(connection_string, db):
    global DB
    print("Connecting to the DB...")
    client = MongoClient(connection_string)
    DB = client[db]


def disconnect():
    print("Disconnecting from the DB...")
    DB.client.close()


def read(collection, query, fields=None, one=False):
    if one:
        return DB[collection].find_one(query, fields)
    else:
        return list(DB[collection].find(query, fields))


def write(collection, query, document, one=False):
    if one:
        DB[collection].update_one(query, document, upsert=True)
    else:
        DB[collection].update_many(query, document)
