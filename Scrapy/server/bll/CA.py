#coding:utf-8
from helpClass.Base import *

class CA(Base):
    """
    Air China Cargo
    """
    def __init__(self):
        super(CA, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:
            headers = self.defaultHeaders()
            urlAirChinaCargoTracking = 'http://www.airchinacargo.com/search_order.php'
            aaCargoPostData = {'trackingPath':'track10'
    ,'orders10':self.type
    ,'orders0':awbNumber
    ,'orders11':''
    ,'orders1[':''
    ,'orders12':''
    ,'orders2':''
    ,'orders13':''
    ,'orders3':''
    ,'orders14':''
    ,'orders4':''
    ,'orders9':''
    ,'section':'0-0001-0003-0081'
    ,'x[6]':'0'
    ,'y[6]':'0'}
       
            
            htmlSource = self.httPost(urlAirChinaCargoTracking,aaCargoPostData,self.coding.UTF_8,headers)
            pattern = r'<tr.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>'
            match = re.findall(pattern, htmlSource,re.DOTALL | re.IGNORECASE)

            rcsType = 'RCS'
            rcfType = 'RCF'
            rcsNumber = 0
            rcfNumber = 0

            dictionaryData = {}
            for x in match:
                if rcsType.upper() in x[0].upper():     #状态名称format by RCS(货物收运)
                    rcsNumber = int(x[2].strip())
                    dictionaryData['ATD'] = match[1][5].strip()
                    dictionaryData['MAWB_NO'] = '-'.join((self.type,awbNumber))
                if rcfType.upper() in x[0].upper():
                    rcfNumber = rcfNumber + int(x[2].strip())

            if rcsNumber == rcfNumber and rcsNumber <> 0 and rcfNumber != 0:   #当两数相等时候ATD时间出现
                dictionaryData['ATA'] = x[5].strip()
                self.InsertByDictionary(self.analyze_table_name,dictionaryData)
                self.InsertByDocument(self.source_table_name,htmlSource)
            else:
                return self.errorStatus

        except Exception,e:
            return e

    def init(self):
        self.type = '999'
        self.source_table_name = 'ca'
        self.analyze_table_name = 'ca_analyze'