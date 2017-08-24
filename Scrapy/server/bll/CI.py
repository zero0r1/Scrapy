#coding:utf-8
from helpClass.Base import *

class CI(Base):
    """
    China Cargo
    """
    def __init__(self):
        
        super(CI, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:
            headers = self.defaultHeaders()
            urlchinaAairlines = 'https://cargo.china-airlines.com/ccnetv2/content/manage/ShipmentTracking.aspx'

            htmlSource = self.httpGet(urlchinaAairlines,self.coding.UTF_8,headers)

            viewstatePattern = 'name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)"'
            viewstate = re.search(viewstatePattern, htmlSource,re.DOTALL).group(1)

            aaCargoPostData = {'__EVENTTARGET':''
                                ,'__EVENTARGUMENT':''
                                ,'__VIEWSTATE':viewstate
                                ,'__SCROLLPOSITIONX':'0'
                                ,'__SCROLLPOSITIONY':'400'
                                ,'sWord':''
                                ,'ctl00$txtCompanyId':''
                                ,'ctl00$txtUserId':''
                                ,'ctl00$txtPassword':''
                                ,'ctl00$ContentPlaceHolder1$txtAwbPfx':self.type
                                ,'ctl00$ContentPlaceHolder1$txtAwbNum':awbNumber
                                ,'ctl00$ContentPlaceHolder1$btnSearch':'Search'
                                ,'ctl00$hdnLogPath':'/ccnetv2/content/home/addLog.ashx'
                                ,'ctl00$hdnProgName':'/ccnetv2/content/manage/shipmenttracking.aspx'}
       
            
            htmlSource = self.httPost(urlchinaAairlines,aaCargoPostData,self.coding.UTF_8,headers)

            orgin = ''
            destination = ''
            ATD = ''
            ATA = ''
            airport = ''
            
            AWdBlackPattern = r'<span class="AWd_black">\s*Origin\s*<span id="ContentPlaceHolder1_lblOrg">(.*?)</span></span>.*?Destination\s*<span id="ContentPlaceHolder1_lblDes">(.*?)</span></span><br>'
            AWdBlackMatch = re.search(AWdBlackPattern, htmlSource,re.DOTALL | re.IGNORECASE)

            orgin = AWdBlackMatch.group(1)
            destination = AWdBlackMatch.group(2)

            rowPattern = r'<tr id="ContentPlaceHolder1_rpFreightStatus_trRow_\d+.*?">\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblCode_\d+.*?">(?P<Status>.*?)</span></td>\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblFlight_\d+.*?">(?P<Flight>.*?)</span></td>\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblEvnPcs_\d+.*?">(?P<Pieces>.*?)</span></span></td>\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblEvnWgt_\d+.*?">(?P<Weight>.*?)</span></td>\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblEvnApt_\d+.*?">(?P<Port>.*?)</span></td>\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblEvnTime_\d+.*?">(?P<EventTime>.*?)</span></td>\s*</tr>'
            rowMatch = re.finditer(rowPattern, htmlSource,re.DOTALL)

            

            dictionaryData = {}
            for x in sorted(rowMatch, reverse=True):
                dict = x.groupdict()
                if u'Departed'.upper() in dict['Status'].upper() and ATD == '':
                    ATD = dict['EventTime'].replace('(ATAL)','').replace('(ATDL)','').strip()
                    timeFormat = datetime.datetime.strptime(''.join((str(datetime.datetime.now().year),ATD)) ,'%Y%d%b %H:%M')
                    dictionaryData['MAWB'] = '-'.join((self.type,awbNumber))
                    dictionaryData['ATD'] = str(timeFormat)

                if u'Arrived'.upper() in dict['Status'].upper():
                    ATA = dict['EventTime'].replace('(ATAL)','').replace('(ATDL)','').strip()
                    timeFormat = datetime.datetime.strptime(''.join((str(datetime.datetime.now().year),ATA)) ,'%Y%d%b %H:%M')
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
        self.type = '297'
        self.source_table_name = 'ci'
        self.analyze_table_name = 'ci_analyze'

    def defaultHeaders(self):
        self.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        self.headers['Cache-Control'] = 'no-cache'
        self.headers['Accept-Encoding'] = 'gzip, deflate, br'
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2,ja;q=0.2'