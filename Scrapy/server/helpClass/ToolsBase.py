from dbhelp.DBEngine import DBEngine
import re
import logging
import threading
import pandas as pd
import time
import requests
import json

class toolsBase(object):
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
        self.headers = {'accept': '*/*'
            ,'accept-encoding': 'gzip, deflate, sdch'
            ,'accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2,ja;q=0.2'
            ,'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}

    def defaultHeaders(self):
        """
        BASE:获取base的headers info
        """
        return self.headers

    def outputLog(self,message):
        logging.debug('CLASS_NAME:{%s} --- MESSAGE:{%s}' % (type(self).__name__,message))

    def mongoModelToDataFrame(self,mongoModel):
        """
        BASE:MongoDB 读取的json格式转换成为数据表格式类似于C#datatable
        """
        return pd.DataFrame(list(mongoModel))

    def sleep(self,second):
        time.sleep(second)

    def httpGet(self,url,pageencoding=None,headers=None):
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

                if pageencoding != None:
                    page.encoding = pageencoding
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

   
    def httPost(self,url,data,pageencoding=None,headers=None):
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

                if pageencoding != None:
                    page.encoding = pageencoding
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

    def Insert(self,colName,jsonData):
        """
        插入数据capture cargo data
        """
        DBEngine.Insert(colName,jsonData)

    def SaveLog(self,colName,jsonData):
        """
        保存错误日志
        """
        DBEngine.Insert(colName,jsonData)
    #DEF WORKERWITH(SELF,LOCK):
    #    """
    #    开始CAPTURE工作
    #    """
    #    TRY:
    #        AWBNUMBERARRAY = []
    #        AWBNUMBERCACHE = []

    #        #抓取的主单号码(不带3字头编码)
    #        CAPTURENO = 'CAPTURENO'

    #        WHILE TRUE:

    #            WITH LOCK:
    #                WHILE LEN(AWBNUMBERARRAY) == 0 :
    #                        #SELF.OUTPUTLOG('LISTEN DATABASE...')
    #                        SELF.SLEEP(SELF.SLEEPNUM)
    #                        AWBARRAY =
    #                        SELF.GETAWBNUMBERARRAY(SELF.CAPTUREQUEUE)
    #                        AWBNUMBERARRAY =
    #                        SELF.MONGOMODELTODATAFRAME(AWBARRAY)

    #            WITH LOCK:
    #                AWBNUMBER = AWBNUMBERARRAY.ILOC[0][CAPTURENO]
                
    #                IF AWBNUMBER NOT IN AWBNUMBERCACHE:
    #                    AWBNUMBERCACHE.APPEND(AWBNUMBER)
    #                    AWBNUMBERARRAY =
    #                    AWBNUMBERARRAY.LOC[AWBNUMBERARRAY[CAPTURENO] !=
    #                    STR(AWBNUMBER)]
    #                    SELF.UPDATEAWBNUMBERSTATUS(SELF.CAPTUREQUEUE,AWBNUMBER,'C')
    #                    SELF.OUTPUTLOG("MAWB: %S --- START..." % AWBNUMBER)
            
                
    #            RESULTAWBNUMBER = SELF.GETHTMLDATA(AWBNUMBER)

    #            WITH LOCK:
    #                #SELF.OUTPUTLOG("REMOVE %S CACHE..." % AWBNUMBER)
    #                """
    #                D:DONE
    #                W:WAIT
    #                C:CAPTURING
    #                """
    #                AA=
    #                SELF.UPDATEAWBNUMBERSTATUS(SELF.CAPTUREQUEUE,AWBNUMBER,'D')
    #                AWBNUMBERCACHE.REMOVE(AWBNUMBER)
    #    FINALLY:
    #        SELF.OUTPUTLOG('DONE...')
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
                with lock:
                    if error != 'error':
                        self.updateAWBNumberStatus(self.captureQueue,awbNumber,'d')

        finally:
            self.outputLog('capture done...')

    #def getWorkMAWBno(self):
        
    #    while len(self.awbnumberArray) == 0 :
    #            self.outputLog('listen database...')
    #            self.sleep(self.sleepNum)
    #            awbArray = self.getAwbnumberArray(self.captureQueue)
    #            self.awbnumberArray = self.mongoModelToDataFrame(awbArray)

    #            row = next(self.awbnumberArray.iteritems()[1])
    #            return row['']

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