#coding:utf-8
from helpClass.Base import *
import datetime

class NH(Base):
    """
    American Airlines
    """
    def __init__(self):
        
        super(NH, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:
            headers = self.defaultHeaders()
            urlANACargo = 'https://shar.ana.co.jp/eACROSS/shipmentStatusSearch.do'
            postData = {'dispatch':'retrieveMAWBSearchResult'
                            ,'guestEntry':'shipmentStatus'
                            ,'awbType':'MAWB'
                            ,'mawbPrefix1':'205'
                            ,'mawbSuffix1':awbNumber
                            ,'hawbNumber1':''
                        }
       
            
            htmlSource = self.httPost(urlANACargo,postData,self.coding.UTF_8,headers)


            orgin = ''
            destination = ''
            ATD = ''
            ATA = ''
            airport = ''

            tablePattern = r'<tr bgcolor="#FFFFFF" class="b1313">\s*<td.*?>(.*?)</td>\s*<td.*?>(.*?)</td>\s*<td.*?>(.*?)</td>\s*<td.*?>(.*?)</td>\s*<td.*?>(.*?)</td>\s*<td.*?>(.*?)</td>\s*<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>'
            tableMatch = re.findall(tablePattern, htmlSource,re.DOTALL | re.IGNORECASE)

            dictionaryData = {}
            for x in tableMatch:
                if awbNumber in x[0]:
                    """
                     当前的第一行包含了orgin/destination,MAWB信息
                    """
                    orgin = x[1]
                    destination = x[2]

                if orgin in x[0] or destination in x[0]:
                    """
                    此判断为了过滤不是站点信息数据
                    """
                    if u'Departed'.upper() in x[1].upper() and ATD == '' and orgin.upper() == x[0].upper():
                        ATD = x[2] + x[3]
                        timeFormat = datetime.datetime.strptime(ATD,'%d-%b-%Y%H:%M:%S')
                        dictionaryData['MAWB'] = '-'.join((self.type,awbNumber))
                        dictionaryData['ATD'] = str(timeFormat)

                    if u'Arrived'.upper() in x[1].upper() and destination.upper() == x[0].upper():
                        ATA = x[2] + x[3]
                        timeFormat = datetime.datetime.strptime(ATA,'%d-%b-%Y%H:%M:%S')
                        dictionaryData['ATA'] = str(timeFormat)
                        airport = x[0]
                        
            if airport.upper() == destination.upper():
                self.InsertByDictionary(self.analyze_table_name,dictionaryData)
                self.InsertByDocument(self.source_table_name,htmlSource)
            else:
                return self.errorStatus #当返回数据的时候外部调用不更新状态,等待下一次的抓取

        except Exception,e:
            return e

    def init(self):
        self.type = '205'
        self.source_table_name = 'nh'
        self.analyze_table_name = 'nh_analyze'

    def defaultHeaders(self):
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Cache-Control'] = 'no-cache'

        return self.headers