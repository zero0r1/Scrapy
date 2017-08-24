#coding:utf-8
from helpClass.Base import *

class OZ(Base):
    """
    American Airlines
    """
    def __init__(self):
        
        super(OZ, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:
            headers = self.defaultHeaders()
            urlCVCargoTracking = 'https://www.asianacargo.com/tracking/newAirWaybill.do'
            cvCargoPostData = {'globalLang':'En'
                                ,'Prefix':'988'
                                ,'Billno':awbNumber
                                ,'Billno2':''
                                ,'Billno3':''
                                ,'Billno4':''
                                ,'Billno5':''
                                ,'location':'C'
                                ,'T1':''
                                ,'awb_id':''
                                ,'mawb':''
                                ,'cmn':''
                                ,'release':''
                                ,'edi_no_of_release':''
                                ,'hawb':''
                                ,'prefix':''
                                ,'billno':''
                                }
            
            htmlSource = self.httPost(urlCVCargoTracking,cvCargoPostData,None,headers)

            orgin = ''
            destination = ''
            ATD = ''
            ATA = ''
            airport = ''
            
            fonormPattern = r'<div\s*class="point.*?float_l">.*?<h1>(.*?)</h1>'
            fonormMatch = re.finditer(fonormPattern, htmlSource,re.DOTALL | re.IGNORECASE)
            for x in fonormMatch:
                if orgin == '':
                    orgin = x.group(1)
                
                destination = x.group(1)
           

            rowPattern = r'<tr>.*?<td\s*class="txta_l">.*?<div\s*class="status.*?">(?P<Status>.*?)</div>.*?</td>.*?<td>(?P<Flt_No>.*?)</td>.*?<td>(?P<Origin>.*?)</td>.*?<td>(?P<Dest>.*?)</td>.*?<td>(?P<Event_Time>.*?)</td>.*?<td>(?P<Pieces>.*?)</td>.*?<td>(?P<Weight>.*?)</td>'
            rowMatch = re.finditer(rowPattern, htmlSource,re.DOTALL | re.IGNORECASE)

            dictionaryData = {}
            for x in sorted(rowMatch, reverse=False):
                dict = x.groupdict()
                    #Departed
                if u'DEPARTED'.upper() in dict['Status'].upper() and ATD == '': 
                    ATD = dict['Event_Time']
                    timeFormat = datetime.datetime.strptime(''.join((str(datetime.datetime.now().year),ATD)) ,'%Y%b%d%H:%M')
                    dictionaryData['MAWB'] = '-'.join((self.type,awbNumber))
                    dictionaryData['ATD'] = str(timeFormat)
                    #Arrived
                if u'ARRIVED'.upper() in dict['Status'].upper():
                    ATA = dict['Event_Time']
                    timeFormat = datetime.datetime.strptime(''.join((str(datetime.datetime.now().year),ATA)) ,'%Y%b%d%H:%M')
                    dictionaryData['ATA'] = str(timeFormat)
                    airport = dict['Dest']

            if airport.upper() == destination.upper():
                self.InsertByDictionary(self.analyze_table_name,dictionaryData)
                self.InsertByDocument(self.source_table_name,htmlSource)
            else:
                return self.errorStatus #当返回数据的时候外部调用不更新状态,等待下一次的抓取

        except Exception,e:
            return e

    def init(self):
        self.type = '988'
        self.source_table_name = 'oz'
        self.analyze_table_name = 'oz_analyze'