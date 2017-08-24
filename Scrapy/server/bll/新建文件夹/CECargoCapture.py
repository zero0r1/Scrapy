#coding=utf-8
from helpClass.Base import *
from __builtin__ import str

class ceCargoCapture(Base):
    def __init__(self):
        super(ceCargoCapture, self).__init__()
        self.init()

    def getHtmlData(self,awbNumber):

        try:
            self.outputLog('{type}-{awbNumber} start...'.format(type=self.type,awbNumber=awbNumber))

            headers = self.defaultHeaders()
            cargo2CeAirCom = 'http://cargo2.ce-air.com/MU/Service/getawbinfo.aspx?strCul=zh-CN'

            htmlSource = self.httpGet(cargo2CeAirCom,'gb2312',headers)

            viewStatePattern = r'id="__VIEWSTATE" value="(.*?)"'
            viewStateMatch = re.search(viewStatePattern,htmlSource,re.DOTALL | re.MULTILINE)
            viewsStateKey = viewStateMatch.group(1)

            eventvalidationPattern = r'id="__EVENTVALIDATION" value="(.*?)"'
            eventvalidationMatch = re.search(eventvalidationPattern,htmlSource,re.DOTALL | re.MULTILINE)
            eventvalidationKey = eventvalidationMatch.group(1)

            postData = {'__VIEWSTATE':'{__VIEWSTATE}'.format(__VIEWSTATE=viewsStateKey)
,'__EVENTVALIDATION':'{__EVENTVALIDATION}'.format(__EVENTVALIDATION=eventvalidationKey)
,'rowid':'1'
,'clientOffset':'+08:00'
,'clientOffsetMinutes':'-480'
,'txtstrAwbPfx0':'{txtstrAwbPfx0}'.format(txtstrAwbPfx0=self.type)
,'txtstrbum0':'{txtstrbum0}'.format(txtstrbum0=awbNumber)
,'btnQry':'(unable to decode value)'
,'txtMailAddr':''
,'txtStatusCode$__txtSelect':'(unable to decode value)'
,'txtAwbs':''
,'hidStatusCode':''}

            self.outputLog('request web.')
            htmlSource = self.httPost(cargo2CeAirCom,postData,'gb2312',headers)

            tablePattern = r'航段信息(.*?)</table>'
            tableMatch = re.search(tablePattern,htmlSource,re.DOTALL | re.MULTILINE)
            tableHtml = tableMatch.group(1)
            
            print htmlSource

       
         
        except Exception,e:
            self.outputLog('getHtmlData %s' % e)
            return self.errorStatus

    def init(self):
        self.type = '112'