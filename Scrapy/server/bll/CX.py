#coding:utf-8
from helpClass.Base import *
import datetime

class CX(Base):
    """
    American Airlines
    """
    def __init__(self):
        
        super(CX, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:
            headers = self.defaultHeaders()
            urlCAthaypacificcargo = 'http://www.cathaypacificcargo.com/ManageYourShipment/TrackYourShipment/tabid/108/SingleAWBNo/160-{awbNumber}/language/en-US/Default.aspx'.format(awbNumber=awbNumber)
            htmlSource = self.httpGet(urlCAthaypacificcargo,self.coding.UTF_8)

            VIEWSTATEPattern = r'id="__VIEWSTATE"\s*value="(.*?)"'
            VIEWSTATEMatch = re.search(VIEWSTATEPattern, htmlSource,re.DOTALL)

            EVENTVALIDATIONPattern = r'id="__EVENTVALIDATION"\s*value="(.*?)"'
            EVENTVALIDATIONMatch = re.search(EVENTVALIDATIONPattern, htmlSource,re.DOTALL)

            postData = {'StylesheetManager_TSSM':''
                            ,'ScriptManager_TSM':';;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en:eb198dbd-2212-44f6-bb15-882bde414f00:ea597d4b:b25378d2'
                            ,'__EVENTTARGET':'dnn$ctr779$ViewTnT$ctl00$lbtnShowAllShipmentStatus'
                            ,'__EVENTARGUMENT':''
                            ,'__VIEWSTATE':VIEWSTATEMatch.group(1)
                            ,' __VIEWSTATEGENERATOR':'CA0B0334'
                            ,'__VIEWSTATEENCRYPTED':''
                            ,'__EVENTVALIDATION':EVENTVALIDATIONMatch.group(1)
                            ,'dnn$HEADER$dnnSEARCH$txtSearch':''
                            ,'dnn$ctr779$ViewTnT$ctl00$txtAWBPrefix':'160'
                            ,'dnn$ctr779$ViewTnT$ctl00$txtAWBNo':''
                            ,'dnn$ctr779$ViewTnT$ctl00$hfHighLight':'3-3'
                            ,'ScrollTop':'300'
                            ,'__dnnVariable':'{"__scdoff":"1"}'
                        }
       
            
            htmlSource = self.httPost(urlCAthaypacificcargo,postData,self.coding.UTF_8,headers)

            orgin = ''
            destination = ''
            ATD = ''
            ATA = ''
            airport = ''
            
            onepageFormPattern = r'onepage_form_table_awb_width">.*?<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>'
            onepageFormMatch = re.search(onepageFormPattern, htmlSource,re.DOTALL)

            tablePattern = r'onepage_form_table_width">.*?</table>'
            tableMatch = re.search(tablePattern, htmlSource,re.DOTALL)

            rowPattern = r'<tr id="ContentPlaceHolder1_rpFreightStatus_trRow_\d+.*?">\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblCode_\d+.*?">(?P<Status>.*?)</span></td>\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblFlight_\d+.*?">(?P<Flight>.*?)</span></td>\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblEvnPcs_\d+.*?">(?P<Pieces>.*?)</span></span></td>\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblEvnWgt_\d+.*?">(?P<Weight>.*?)</span></td>\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblEvnApt_\d+.*?">(?P<Event_Airport>.*?)</span></td>\s*<td>.*?<span id="ContentPlaceHolder1_rpFreightStatus_lblEvnTime_\d+.*?">(?P<Event_Time>.*?)</span></td>\s*</tr>'
            rowMatch = re.finditer(rowPattern, tableMatch.group(0),re.DOTALL)

            orgin = onepageFormMatch.group(1)
            destination = onepageFormMatch.group(2)

            dictionaryData = {}
            for x in sorted(rowMatch, reverse=False):
                dict = x.groupdict()
                if u'Departed'.upper() in dict['Status'].upper() and ATD == '':
                    ATD = dict['EventTime'].replace('&nbsp;&nbsp;','/').replace(' ','/').strip()
                    timeFormat = datetime.datetime.strptime(ATD,'%d/%b/%Y/%H:%M')
                    dictionaryData['MAWB'] = '-'.join((self.type,awbNumber))
                    dictionaryData['ATD'] = str(timeFormat)

                if u'Arrived'.upper() in dict['Status'].upper():
                    ATA = dict['EventTime'].replace('&nbsp;&nbsp;','/').replace(' ','/').strip()
                    timeFormat = datetime.datetime.strptime(ATA,'%d/%b/%Y/%H:%M')
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
        self.type = '160'
        self.source_table_name = 'cx'
        self.analyze_table_name = 'cx_analyze'

    def defaultHeaders(self):
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Cache-Control'] = 'no-cache'

        return self.headers