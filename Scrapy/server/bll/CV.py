#coding:utf-8
from helpClass.Base import *

class CV(Base):
    """
    Luxair Cargo
    """
    def __init__(self):
        
        super(CV, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:
            headers = self.defaultHeaders()
            urlCVCargoTracking = 'http://cdmp.champ.aero/ttwfe/search.do'
            cvCargoPostData = {'awbnumber':'172-' + awbNumber
                                ,'requester':'CV'
                                }
            
            htmlSource = self.httPost(urlCVCargoTracking,cvCargoPostData,self.coding.UTF_8,headers)

            orgin = ''
            destination = ''
            ATD = ''
            ATA = ''
            airport = ''
            
            fonormPattern = r'ORG:</div>.*?<div>(.*?)\s*-\s*<span\s*class="fonorm">.*?DEST:</div>.*?<div>(.*?)\s*-\s*<'
            fonormMatch = re.search(fonormPattern, htmlSource,re.DOTALL | re.IGNORECASE)

            orgin = fonormMatch.group(1)
            destination = fonormMatch.group(2)

            rowPattern = r'<tr\s*class="supportedStatus">.*?<td>(?P<Port>.*?)</td>.*?<td>(?P<Status>.*?)</td>.*?<td>.*?<div.*?>(?P<EventTime>.*?)</div>.*?</td>.*?<td><div.*?>(?P<Received_time>.*?)</div>.*?</td>.*?<td><div.*?>(?P<PCS>.*?)</div>.*?</td>.*?<td><div.*?>(?P<WGT>.*?)</div></td>'
            rowMatch = re.finditer(rowPattern, htmlSource,re.DOTALL)

            dictionaryData = {}
            for x in sorted(rowMatch, reverse=True):
                dict = x.groupdict()
                    #Departed
                if u'DEP'.upper() in dict['Status'].upper() and ATD == '': 
                    ATD = dict['Received_time']
                    timeFormat = datetime.datetime.strptime(''.join((str(datetime.datetime.now().year),ATD)) ,'%Y%d%b%H:%M')
                    dictionaryData['MAWB'] = '-'.join((self.type,awbNumber))
                    dictionaryData['ATD'] = str(timeFormat)
                    #Arrived
                if u'ARR'.upper() in dict['Status'].upper():
                    ATA = dict['Received_time']
                    timeFormat = datetime.datetime.strptime(''.join((str(datetime.datetime.now().year),ATA)) ,'%Y%d%b%H:%M')
                    dictionaryData['ATA'] = str(timeFormat)
                    airport = dict['Port']

            if airport.upper() == destination.upper():
                self.InsertByDictionary(self.analyze_table_name,dictionaryData)
                self.InsertByDocument(self.source_table_name,htmlSource)
            else:
                return self.errorStatus #当返回数据的时候外部调用不更新状态,等待下一次的抓取

        except Exception,e:
            return e

    def init(self):
        self.type = '172'
        self.source_table_name = 'cv'
        self.analyze_table_name = 'cv_analyze'