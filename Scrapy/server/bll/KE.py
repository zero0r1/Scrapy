#coding:utf-8
from helpClass.Base import *

class KE(Base):
    """
    American Airlines
    """
    def __init__(self):
        
        super(KE, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:
            headers = self.defaultHeaders()
            cargoKoreanairCom = 'http://cargo.koreanair.com/ecus/trc/servlet/TrackingServlet'
            postData = {'pid':'5'
,'version':'eng'
,'awb_no':''.join((self.type,awbNumber))
,'multiAwbNo':''.join((self.type,awbNumber))
,'menu1':'m1'
,'menu2':'m01-1'
,'preAwbNo':self.type
,'version':'eng'
,'postAwbNo':awbNumber}
       
            
            htmlSource = self.httPost(cargoKoreanairCom,postData,self.coding.ISO_8859_1,headers)
            pattern = r'Cargo Status.*?<!-- offload'
            match = re.search(pattern, htmlSource,re.DOTALL)

            offloadTable = match.group(0)
            offloadTablePattern = r'<tr.*?>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>'
            offloadTableMatch = re.findall(offloadTablePattern, offloadTable,re.DOTALL)

            
            orgin = ''
            destination = ''
            ATD = ''
            ATA = ''
            airport = ''

            orgDesPattern = r'Orgin/Destination</td>\s*<td.*?>(.*?)</td>'
            orgDesMatch = re.search(orgDesPattern, htmlSource,re.DOTALL)
            orgDesString = orgDesMatch.group(1)
            orgin = orgDesString.split('/')[0].strip()
            destination = orgDesString.split('/')[1].strip()

            dictionaryData = {}
            for x in offloadTableMatch:
                if u'Departed'.upper() in x[1].upper():
                    ATD = x[3]
                    dictionaryData['MAWB'] = '-'.join((self.type,awbNumber))
                    dictionaryData['ATD'] = ATD
                
                if u'Arrived'.upper() in x[1].upper():
                    ATA = x[3]
                    dictionaryData['ATA'] = ATA
                    airport = x[6]

            if airport.upper() == destination.upper():
                self.InsertByDictionary(self.analyze_table_name,dictionaryData)
                self.InsertByDocument(self.source_table_name,htmlSource)
            else:
                return self.errorStatus
                
        except Exception,e:
            return e

    def init(self):
        self.type = '180'
        self.source_table_name = 'ke'
        self.analyze_table_name = 'ke_analyze'