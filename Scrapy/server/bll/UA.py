#coding:utf-8
from helpClass.Base import *
import datetime

class UA(Base):
    """
    American Airlines
    """
    def __init__(self):
        
        super(UA, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:
            headers = self.defaultHeaders()
            urlUnitedcargoCargo = 'http://booking.unitedcargo.com/skychain/app'
            postData = {'service':'direct/1/nwp:Trackshipmt/trackForm'
                            ,'sp':'S1'
                            ,'Form1':'selectDoctype,txtPrefix,txtNumber,txtJrn,txtAWBPrefix,txtAWBNumber,txtAWBPrefix$0,txtAWBNumber$0,txtAWBPrefix$1,txtAWBNumber$1,txtAWBPrefix$2,txtAWBNumber$2,txtAWBPrefix$3,txtAWBNumber$3,txtAWBPrefix$4,txtAWBNumber$4,txtAWBPrefix$5,txtAWBNumber$5,txtAWBPrefix$6,txtAWBNumber$6,txtAWBPrefix$7,txtAWBNumber$7,$JSubmit,$JSubmit$0,$JSubmit$1,$JSubmit$2,$FormConditional,trackShiptable,hdnSelectedTag,hdnSelectedTableRow,trackShiptable1,hdnSelectedTag$0,hdnSelectedTableRow$0,$FormConditional$0,pageSize,listSize,advSearch,trackViewHdn'
                            ,'trackForm_hdnLastPermissionCheck':'Y'
                            ,'trackForm_hdnLastPermissionCode':''
                            ,'hdnFormID':'trackForm'
                            ,'$FormConditional':'T'
                            ,'hdnSelectedTag':''
                            ,'hdnSelectedTableRow':'java.lang.Long~4430231'
                            ,'hdnSelectedTag$0':''
                            ,'hdnSelectedTableRow$0':'java.lang.Long~4430231'
                            ,'$FormConditional$0':'F'
                            ,'pageSize':'100'
                            ,'listSize':'1'
                            ,'advSearch':'F'
                            ,'trackViewHdn':'tableRadio'
                            ,'selectDoctype':'AWB'
                            ,'txtPrefix':'016'
                            ,'txtNumber':awbNumber
                            ,'txtJrn':''
                            ,'txtAWBPrefix':'016'
                            ,'txtAWBNumber':''
                            ,'txtAWBPrefix':'016'
                            ,'txtAWBNumber':''
                            ,'txtAWBPrefix':'016'
                            ,'txtAWBNumber':''
                            ,'txtAWBPrefix':'016'
                            ,'txtAWBNumber':''
                            ,'txtAWBPrefix':'016'
                            ,'txtAWBNumber':''
                            ,'txtAWBPrefix':'016'
                            ,'txtAWBNumber':''
                            ,'txtAWBPrefix':'016'
                            ,'txtAWBNumber':''
                            ,'txtAWBPrefix':'016'
                            ,'txtAWBNumber':''
                            ,'txtAWBPrefix':'016'
                            ,'txtAWBNumber':''
                            ,'$JSubmit$0':'Track'
                            ,'trackShiptableDataRow0':'java.lang.Long~4430231'
                            ,'trackShiptableJavaClass':'com.emirates.ngcs.nweb.trackshipment.ShipmentDTO'
                            ,'trackShiptable1DataRow0':'java.lang.Long~4430231'
                            ,'trackShiptable1JavaClass':'com.emirates.ngcs.nweb.trackshipment.ShipmentDTO'
                        }
       
            
            htmlSource = self.httPost(urlUnitedcargoCargo,postData,self.coding.UTF_8,headers)

            if 'session has timed out' in htmlSource:
                htmlSource = self.httPost(urlUnitedcargoCargo,postData,self.coding.UTF_8,headers)

            htmlSource = htmlSource.replace('&nbsp;','').replace('</span>','')
            tablePattern = r'<table\s*name="trackShiptable1(.*?)</table>'
            tableMatch = re.search(tablePattern, htmlSource,re.DOTALL)

            orgin = ''
            destination = ''
            ATD = ''
            ATA = ''
            airport = ''
            
            OriginDestPattern = r'<tr.*?>.*?<td.*?>(.*?)</td>\s*<td class="grdRowData">(.*?)</td>\s*<td class="grdRowData">(.*?)</td>\s*<td class="grdRowData">(.*?)</td>\s*<td class="grdRowData">(.*?)</td>\s*<td class="grdRowData">(.*?)</td>\s*<td class="grdRowData">(.*?)</td>\s*<td class="grdRowData">(.*?)</td>\s*<td class="grdRowData">(.*?)</td></tr>'
            OriginDestMatch = re.search(OriginDestPattern, tableMatch.group(0),re.DOTALL)
            orgin = OriginDestMatch.group(3)
            destination = OriginDestMatch.group(4)

            rowPattern = r'<tr class="grdRow"><td class="grdNobg">(?P<Station>.*?)</td><td class="grdRowData">(?P<Status_Date_Time>.*?)</td><td class="grdRowData">(?P<Status>.*?)</td><td class="grdRowData">(?P<Flight_Details>.*?)</td><td class="grdRowData">(?P<Pieces>.*?)</td><td class="grdRowData">(?P<Weight>.*?)</td></tr>'
            rowMatch = re.finditer(rowPattern, tableMatch.group(0),re.DOTALL)

            dictionaryData = {}
            for x in rowMatch:
                dict = x.groupdict()
                if u'Departed'.upper() in dict['Status'].upper() and ATD == '' and dict['Station'].upper() == orgin.upper():
                    ATD = dict['Status_Date_Time'].strip().replace(' ','/')
                    timeFormat = datetime.datetime.strptime(ATD,'%d/%b/%Y/%H:%M')
                    dictionaryData['MAWB'] = '-'.join((self.type,awbNumber))
                    dictionaryData['ATD'] = str(timeFormat)

                if u'Arrived'.upper() in dict['Status'].upper() and dict['Station'].upper() == destination.upper():
                    ATA = dict['Status_Date_Time'].strip().replace(' ','/')
                    timeFormat = datetime.datetime.strptime(ATA,'%d/%b/%Y/%H:%M')
                    dictionaryData['ATA'] = str(timeFormat)
                    airport = dict['Station']

            if airport.upper() == destination.upper():
                self.InsertByDictionary(self.analyze_table_name,dictionaryData)
                self.InsertByDocument(self.source_table_name,htmlSource)
            else:
                return self.errorStatus #当返回数据的时候外部调用不更新状态,等待下一次的抓取

        except Exception,e:
            return e

    def init(self):
        self.type = '016'
        self.source_table_name = 'ua'
        self.analyze_table_name = 'ua_analyze'

    def defaultHeaders(self):
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Cache-Control'] = 'no-cache'

        return self.headers