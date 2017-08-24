from  dbhelp import db
import json

class DBEngine(object):
    @staticmethod
    def Insert(colName,jsonData):
        convertJson = json.loads(jsonData)
        db[colName].insert_one(convertJson)

    @staticmethod
    def getCaptureData(colName,type,filter,limit):
        return db[colName].find({'captureStatus':str(filter),'type':str(type)}).limit(limit)

    @staticmethod
    def updateCaptureStatus(colName,type,awbNumber,status):
        return db[colName].update_one({'captureNo':awbNumber,'type':type},{'$set': {'captureStatus': status}})

    @staticmethod
    def findAndModify(colName,type,filter):
        return db[colName].find_and_modify({'captureStatus':str(filter),'type':str(type)}
                                           ,{'$set': {'captureStatus': "c"}}
                                           ,multi=True)