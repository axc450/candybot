from pymongo import MongoClient
from pymongo.database import Database


_DB: Database = None


def connect(connection_string, db):
    global _DB
    print("Connecting to the DB...")
    client = MongoClient(connection_string)
    _DB = client[db]


def disconnect():
    print("Disconnecting from the DB...")
    _DB.client.close()


def read(request):
    print("DB READ " + request.collection)
    if request.query:
        query = request.query
    else:
        query = {"_id": request.server} if request.server else {}
    if request.one:
        return _DB[request.collection].find_one(query, request.fields)
    else:
        return list(_DB[request.collection].find(query, request.fields))


def write(request):
    print("DB WRITE " + request.collection)
    query = {"_id": request.server}
    document = {"$set": request.json}
    _DB[request.collection].update_one(query, document, upsert=True)
