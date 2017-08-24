#coding:utf-8
from helpClass.Base import *
import datetime

class EK(Base):
    """
    American Airlines
    """
    def __init__(self):
        
        super(EK, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:
            headers = self.defaultHeaders()
            urlEmiratesCargo = 'http://skychain.emirates.com/skychain/app'
            postData = {'service':'direct/1/nwp:Trackshipmt/trackForm'
                            ,'sp':'S0'
                            ,'Form0':'txtPrefix,txtNumber,txtJrn,txtAWBPrefix,txtAWBNumber,txtAWBPrefix$0,txtAWBNumber$0,txtAWBPrefix$1,txtAWBNumber$1,txtAWBPrefix$2,txtAWBNumber$2,txtAWBPrefix$3,txtAWBNumber$3,txtAWBPrefix$4,txtAWBNumber$4,txtAWBPrefix$5,txtAWBNumber$5,txtAWBPrefix$6,txtAWBNumber$6,txtAWBPrefix$7,txtAWBNumber$7,$Submit,reset,$FormConditional,trackShiptable,hdnSelectedTag,hdnSelectedTableRow,trackShiptable1,hdnSelectedTag$0,hdnSelectedTableRow$0,$FormConditional$0,pageSize,listSize,advSearch,trackViewHdn'
                            ,'trackForm_hdnLastPermissionCheck':''
                            ,'trackForm_hdnLastPermissionCode':''
                            ,'hdnFormID':'trackForm'
                            ,'excludeServerValidation':'false'
                            ,'$FormConditional':'T'
                            ,'hdnSelectedTag':''
                            ,'hdnSelectedTableRow':'java.lang.Long~28892494'
                            ,'hdnSelectedTag$0':''
                            ,'hdnSelectedTableRow$0':'java.lang.Long~28892494'
                            ,'$FormConditional$0':'F'
                            ,'pageSize':'10'
                            ,'listSize':'1'
                            ,'advSearch':'F'
                            ,'trackViewHdn':'tableRadio'
                            ,'txtPrefix':'176'
                            ,'txtNumber':awbNumber
                            ,'txtJrn':''
                            ,'txtAWBPrefix':'176'
                            ,'txtAWBNumber':''
                            ,'txtAWBPrefix$0':'176'
                            ,'txtAWBNumber$0':''
                            ,'txtAWBPrefix$1':'176'
                            ,'txtAWBNumber$1':''
                            ,'txtAWBPrefix$2':'176'
                            ,'txtAWBNumber$2':''
                            ,'txtAWBPrefix$3':'176'
                            ,'txtAWBNumber$3':''
                            ,'txtAWBPrefix$4':'176'
                            ,'txtAWBNumber$4':''
                            ,'txtAWBPrefix$5':'176'
                            ,'txtAWBNumber$5':''
                            ,'txtAWBPrefix$6':'176'
                            ,'txtAWBNumber$6':''
                            ,'txtAWBPrefix$7':'176'
                            ,'txtAWBNumber$7':''
                            ,'$Submit':'Track'
                            ,'trackView':'tableRadio'
                            ,'trackShiptableDataRow0':'java.lang.Long~28892494'
                            ,'trackShiptableJavaClass':'com.emirates.ngcs.nweb.trackshipment.ShipmentDTO'
                            ,'trackShiptable1DataRow0':'java.lang.Long~28892494'
                            ,'trackShiptable1JavaClass':'com.emirates.ngcs.nweb.trackshipment.ShipmentDTO'
                        }
       
            
            htmlSource = self.httPost(urlEmiratesCargo,postData,self.coding.UTF_8,headers)

            if 'session timed out' in htmlSource:
                htmlSource = self.httPost(urlEmiratesCargo,postData,self.coding.UTF_8,headers)

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

            rowPattern = r'<tr class="(?:grdRow|grdRowAlternate)"><td class=".*?">(?P<Station>.*?)</td><td class=".*?">(?P<Status_Date_Time>.*?)</td><td class=".*?">(?P<Status>.*?)</td><td class=".*?">(?P<Flight_Details>.*?)</td><td class=".*?">(?P<Pieces>.*?)</td><td class=".*?">(?P<Weight>.*?)</td></tr>'
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
        self.type = '176'
        self.source_table_name = 'ek'
        self.analyze_table_name = 'ek_analyze'

    def defaultHeaders(self):
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Cache-Control'] = 'no-cache'

        return self.headers