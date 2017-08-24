from pymongo import MongoClient

uri = "mongodb://admin:sa@localhost/dbtest?authMechanism=SCRAM-SHA-1"
client = MongoClient(uri)
db = client.dbtest