#coding:utf-8
from helpClass.Base import *

class MU(Base):
    """
    中国东方航空
    """
    def __init__(self):
        super(MU, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:

            headers = self.defaultHeaders()
            cargo2CeAirCom = 'http://cargo2.ce-air.com/MU/Service/getawbinfo.aspx?strCul=zh-CN'

            htmlSource = self.httpGet(cargo2CeAirCom,self.coding.GB2312,headers)

            viewStatePattern = r'id="__VIEWSTATE" value="(.*?)"'
            viewStateMatch = re.search(viewStatePattern,htmlSource,re.DOTALL | re.IGNORECASE)
            viewsStateKey = viewStateMatch.group(1)

            eventvalidationPattern = r'id="__EVENTVALIDATION" value="(.*?)"'
            eventvalidationMatch = re.search(eventvalidationPattern,htmlSource,re.DOTALL | re.IGNORECASE)
            eventvalidationKey = eventvalidationMatch.group(1)

            postData = {'__VIEWSTATE':viewsStateKey
,'__EVENTVALIDATION':eventvalidationKey
,'rowid':'1'
,'clientOffset':'+08:00'
,'clientOffsetMinutes':'-480'
,'txtstrAwbPfx0':self.type
,'txtstrbum0':awbNumber
,'btnQry':'(unable to decode value)'
,'txtMailAddr':''
,'txtStatusCode$__txtSelect':'(unable to decode value)'
,'txtAwbs':''
,'hidStatusCode':''}

            
            htmlSource = self.httPost(cargo2CeAirCom,postData,self.coding.GB2312,headers)

            tablePattern = ur'航段信息(.*?)</table>'
            tableMatch = re.search(tablePattern,htmlSource,re.DOTALL | re.IGNORECASE)
            tableHtml = tableMatch.group(1)
            
            rowPanttern = ur'<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>'
            rowMatch = re.findall(rowPanttern,tableHtml,re.DOTALL | re.IGNORECASE)
            
            ATD = ''
            ATA = ''
            for x in rowMatch:
                ATD = x[4].replace('&nbsp;','')
                ATA = x[5].replace('&nbsp;','')
    
            if ATD <> '' and ATA <> '':
                dictionaryData = {}
                dictionaryData['ATA'] = ATA[0:4] + '-' + ATA[4:6] + '-' + ATA[6:8] + ATA[8:]    #yyy-MM-dd hh:mm
                dictionaryData['ATD'] = ATD[0:4] + '-' + ATD[4:6] + '-' + ATD[6:8] + ATD[8:]    #yyy-MM-dd hh:mm
                dictionaryData['MAWB'] = '-'.join((self.type,awbNumber))
                self.InsertByDictionary(self.analyze_table_name,dictionaryData)
                self.InsertByDocument(self.source_table_name,htmlSource)
            else:
                return self.errorStatus
         
        except Exception,e:
            return e

    def init(self):
        self.type = '112'
        self.source_table_name = 'cz'
        self.analyze_table_name = 'cz_analyze'