from httphelp.HttpHelper import httpHelper
from httphelp.HttpBase import httpBase
from bs4 import BeautifulSoup
import requests
import re
from dbhelp.AAcargo import AAcargo
import logging


class captureAACargo(httpBase):

    def getHtmlData(self,awbNumber):
        try:
            session = requests.session()
            headers = self.defaultHeaders()
            urlAACargoTracking = 'https://www.aacargo.com/AACargo/tracking'
            aaCargoPostData = {'trackingPath':'track10'
    ,'airwayBills[0].awbCode':'001'
    ,'airwayBills[0].awbNumber':'%s' % awbNumber
    ,'airwayBills[1].awbCode':''
    ,'airwayBills[1].awbNumber':''
    ,'airwayBills[2].awbCode':''
    ,'airwayBills[2].awbNumber':''
    ,'airwayBills[3].awbCode':''
    ,'airwayBills[3].awbNumber':''
    ,'airwayBills[4].awbCode':''
    ,'airwayBills[4].awbNumber':''
    ,'airwayBills[5].awbCode':''
    ,'airwayBills[5].awbNumber':''
    ,'airwayBills[6].awbCode':''
    ,'airwayBills[6].awbNumber':''
    ,'airwayBills[7].awbCode':''
    ,'airwayBills[7].awbNumber':''
    ,'airwayBills[8].awbCode':''
    ,'airwayBills[8].awbNumber':''
    ,'airwayBills[9].awbCode':''
    ,'airwayBills[9].awbNumber':''
    ,'track10Search':'Track'}
       
            logging.debug('request web.')
            htmlSource = httpHelper.httPost(urlAACargoTracking,aaCargoPostData,session,'ISO-8859-1',headers)

            logging.debug('analyze web data and find number')
            pattern = r'<!-- ACTION LINKS -->.*<input\stype="hidden"\svalue="(\d{8})"'
            match = re.search(pattern, htmlSource,re.DOTALL)

            firstOneMawbNO = match.group(1)

            logging.debug('request aacargo json data')
            urlMasterAirWayBillDetails = 'https://www.aacargo.com/AACargo/tracking/masterAirWayBillDetails?airwayBillId=<airwayBillId>'.replace('<airwayBillId>',firstOneMawbNO)
            masterAirWayBillDetailsSource = httpHelper.httpGet(urlMasterAirWayBillDetails,session,'ISO-8859-1',headers)

            logging.debug('save data to the data base')
            AAcargo.Insert(masterAirWayBillDetailsSource)
        
            logging.debug('%s done.' % awbNumber)
        except Exception,e:
            logging.debug('getHtmlData %s' % e)
            return awbNumber

    def defaultHeaders(self):
        return self.headers