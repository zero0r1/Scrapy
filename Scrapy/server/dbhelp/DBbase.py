from pymongo import MongoClient

class DBbase(object):

        @staticmethod
        def ConnectionDB():
            uri = "mongodb://admin:sa@localhost/dbtest?authMechanism=SCRAM-SHA-1"
            client = MongoClient(uri)
            db = client.dbtest
            return db;