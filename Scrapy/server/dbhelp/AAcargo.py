from DBbase import DBbase
import json

class AAcargo(object):
    @staticmethod
    def Insert(jsonData):
        db = DBbase.ConnectionDB()
        convertJson = json.loads(jsonData)
        db.aacargo.insert_one(convertJson)

    @staticmethod
    def get_capture_data(filter,limit):
        db = DBbase.ConnectionDB()
        return db.capture_queue.find({'captureStatus':filter}).limit(limit)

    @staticmethod
    def update_capture_status(awbNumber,status):
        db = DBbase.ConnectionDB()
        return db.capture_queue.update_one({'captureNo':awbNumber},{'$set': {'captureStatus': status}})