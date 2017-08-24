#coding:utf-8
from helpClass.Base import *
import datetime

class RU(Base):
    """
    American Airlines
    """
    def __init__(self):
        
        super(RU, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:
            headers = self.defaultHeaders()
            cargoKoreanairCom = 'http://www.airbridgecargo.com/en/tracking/'
            postData = {'prefix':self.type
                        ,'trackid':awbNumber
                        }
       
            
            htmlSource = self.httPost(cargoKoreanairCom,postData,self.coding.UTF_8,headers)
            infomationPattern = r'<tr\s*class="(?:\s*tr_firsttr_light\s*|\s*tr_light\s*)*">\s*<td>(?P<Station>.*?)</td>\s*<td\s*class="status">(?P<Status>.*?)</td>\s*<td\s*class="date">(?P<EventTime>.*?)</td>\s*<td\s*class="date">(?P<Description>.*?)</td>\s*<!--.*?-->\s*<td\s*class="pieces">(?P<Pieces>.*?)</td>\s*<td\s*class="weight">(?P<Weight>.*?)</td>.*?</tr>'
            r = re.compile(infomationPattern,re.DOTALL | re.IGNORECASE)
            
            orgin = ''
            destination = ''
            ATD = ''
            ATA = ''
            airport = ''

            orgDesPattern = r'Origin:\s*</td>\s*<td>\s*<strong>(.*?)</strong>.*?Destination:\s*</td>\s*<td>\s*<strong>(.*?)</strong>'
            orgDesMatch = re.search(orgDesPattern, htmlSource,re.DOTALL)
            orgin = orgDesMatch.group(1)
            destination = orgDesMatch.group(2)

            dictionaryData = {}
            for x in sorted(r.finditer(htmlSource), reverse=True):
                dict = x.groupdict()
                if u'Departed'.upper() in dict['Status'].upper() and ATD == '':
                    ATD = dict['EventTime'].replace('&nbsp;','').strip()
                    dictionaryData['MAWB'] = '-'.join((self.type,awbNumber))
                    dictionaryData['ATD'] = ATD[0:7] + ' ' + ATD[7:]
                
                if u'Arrived'.upper() in dict['Status'].upper():
                    ATA = dict['EventTime'].replace('&nbsp;','').strip()
                    dictionaryData['ATA'] = ATA[0:7] + ' ' + ATA[7:]
                    airport = dict['Station']

            if airport.upper() == destination.upper():
                self.InsertByDictionary(self.analyze_table_name,dictionaryData)
                self.InsertByDocument(self.source_table_name,htmlSource)
            else:
                return self.errorStatus
                
        except Exception,e:
            return e

    def init(self):
        self.type = '580'
        self.source_table_name = 'ru'
        self.analyze_table_name = 'ru_analyze'