#coding:utf-8
from dbhelp.DBEngine import DBEngine
import re
import logging
import threading
import pandas as pd
import time
import requests
import json
from enum import Enum
from __builtin__ import str,int
import datetime

class CodingEnum(Enum):
    UTF_8 = 'UTF-8'
    ISO_8859_1 = 'ISO-8859-1'
    GB2312 = 'GB2312'


class Base(object):
    def __init__(self):
        #数据队列表
        self.captureQueue = 'capture_queue'
        #睡眠时间1秒
        self.sleepNum = 1
        #数据库读取数量10个
        self.limitNum = 10
        #线程数量1个
        self.threadNum = 1
        #http session
        self.session = requests.session()
        #类名
        self.className = ''
        #http headers info
        self.type = ''
        #主单的行
        self.awbNoRow = None
        self.timeOut = 10
        self.errorStatus = 'error'
        #html source code
        self.source_table_name = ''
        #html analyze data
        self.analyze_table_name = ''
        self.headers = {'accept': '*/*'
            ,'accept-encoding': 'gzip, deflate, sdch'
            ,'accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2,ja;q=0.2'
            ,'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
        #设置编码枚举
        self.coding = CodingEnum

    def defaultHeaders(self):
        """
        BASE:获取base的headers info
        """
        return self.headers

    def outputLog(self,message):
        logging.warning('CLASS_NAME:{%s} --- MESSAGE:{%s}' % (type(self).__name__,message))

    def mongoModelToDataFrame(self,mongoModel):
        """
        BASE:MongoDB 读取的json格式转换成为数据表格式类似于C#datatable
        """
        return pd.DataFrame(list(mongoModel))

    def sleep(self,second):
        time.sleep(second)

    def filterCharset(func):
        def _filterCharset(*args, **kwargs):
            ret = func(*args, **kwargs)
            
            for x in ['\t', '\r', '\n', '&nbsp;', ' ']:
                ret = ret.replace(x,'')

            return ret
        return _filterCharset

    @filterCharset
    def httpGet(self,url,pageEncoding=None,headers=None):
        """
        BASE:使用http get协议读取html页面
        """
        exceptNumber = 0
        while True:
            try:

                if headers != None:
                     page = self.session.get(url,headers=headers,timeout=self.timeOut)
                else:
                     page = self.session.get(url,timeout=self.timeOut)

                if pageEncoding != None:
                    page.encoding = pageEncoding
                    return page.text

                return page.text

            except Exception,e:
                 self.outputLog('httpGet %s' % e)
                 #timeOut some code
                 exceptNumber = exceptNumber + 1
                 if exceptNumber > 3:
                    log = {}
                    log['url'] = url
                    log['log_info'] = str(e)
                    json_data = json.dumps(log)
                    self.SaveLog('log',json_data)
                    return ''

    @filterCharset
    def httPost(self,url,data,pageEncoding=None,headers=None):
        """
        BASE:使用http post协议读取html页面
        """
        exceptNumber = 0
        while True:
            try:

                if headers != None:
                     page = self.session.post(url,data=data,headers=headers,timeout=self.timeOut)
                else:
                     page = self.session.post(url,data=data,timeout=self.timeOut)

                if pageEncoding != None:
                    page.encoding = pageEncoding
                    return page.text

                return page.text

            except Exception,e:
                self.outputLog('httPost %s' % e)
                #timeOut some code
                exceptNumber = exceptNumber + 1
                if exceptNumber > 3:
                    log = {}
                    log['url'] = url
                    log['log_info'] = str(e)
                    log['data'] = json.dumps(data)
                    json_data = json.dumps(log)
                    self.SaveLog('log',json_data)
                    return ''

    def getSession(self):
        return self.session
    def getAwbnumberArray(self,colName):
        """
        获取Cargo抓取队列数据
        """
        return DBEngine.getCaptureData(colName,self.type,'w',self.limitNum)

    def updateAWBNumberStatus(self,colName,awbNumber,status):
        """
        更新Cargo数据状态
        d:DONE
        w:WAIT
        c:CAPTURING
        """
        return DBEngine.updateCaptureStatus(colName,self.type,awbNumber,status)

    def Insert(self,tableName,jsonData):
        """
        插入数据capture cargo data
        """
        DBEngine.Insert(tableName,jsonData)

    def InsertByDictionary(self,tableName,dictionary):
        """
        插入数据capture cargo data
        """
        jsonData = json.dumps(dictionary)
        DBEngine.Insert(tableName,jsonData)

    def InsertByDocument(self,tableName,document):
        """
        插入数据capture cargo data
        """
        array = {}
        array[0] = document
        jsonData = json.dumps(array)
        DBEngine.Insert(tableName,jsonData)

    def SaveLog(self,colName,jsonData):
        """
        保存错误日志
        """
        DBEngine.Insert(colName,jsonData)

    def workerWith(self,lock):
        """
        开始capture工作
        """
        try:
            #抓取的主单号码(不带3字头编码)
            captureNo = 'captureNo'
            awbnumberArray = []
            
            while True:
                with lock:
                    while len(awbnumberArray) == 0 :
                        self.outputLog('listen database...')
                        self.sleep(self.sleepNum)
                        awbArray = self.getAwbnumberArray(self.captureQueue)
                        awbnumberArray = self.mongoModelToDataFrame(awbArray)
                        self.awbNoRow = awbnumberArray.iterrows()

                with lock:
                    try:
                        row = next(self.awbNoRow,None)[1]
                        awbNumber = row[captureNo]
                        type = row['type']
                    except:
                        awbnumberArray = []
                        continue

                error = self.getHtmlData(awbNumber)

                #当没有错误信息的时候更新状态,否则不更新
                #with lock:
                #    if error != self.errorStatus:
                        #self.updateAWBNumberStatus(self.captureQueue,awbNumber,'d')

        finally:
            self.outputLog('capture done...')

    def startCapture(self):
        """
        启动线程
        """
        lock = threading.Lock()
        global awbNoRow
        for x in range(self.threadNum):
            #self.outputLog("thread start...")
            thread = threading.Thread(target=self.workerWith, args=(lock,))
            #是否设置是后台线程
            #thread.setDaemon(True)
            thread.start()
        

def opinfo(func):
    def _opinfo(*args, **kwargs):
        logging.warning('CLASS:{className}   {type}-{awbNumber} start...'.format(type=args[0].type,awbNumber=args[1],className=func.func_globals['__name__']))
        ret = func(*args, **kwargs)

        if ret == '' or ret == None:
            logging.warning('CLASS:{className}   {type}-{awbNumber} done.'.format(type=args[0].type,awbNumber=args[1],className=func.func_globals['__name__']))
        else:
            logging.warning('{funcName}:{error}'.format(funcName=func.__name__,error=ret))

        return ret
    return _opinfo


