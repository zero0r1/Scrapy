#coding:utf-8
from helpClass.Base import *

class Y8(Base):
    """
    中国东方航空
    """
    def __init__(self):
        super(Y8, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:

            headers = self.defaultHeaders()
            cargoitranYzrComCn = 'http://cargoitran.yzr.com.cn/SearchFlight/QueryAWB.aspx'

            htmlSource = self.httpGet(cargoitranYzrComCn,self.coding.UTF_8,headers)

            viewStatePattern = r'id="__VIEWSTATE" value="(.*?)"'
            viewStateMatch = re.search(viewStatePattern,htmlSource,re.DOTALL | re.IGNORECASE)
            viewsStateKey = viewStateMatch.group(1)

            postData = {'__VIEWSTATE':viewsStateKey
                        ,'ctl00$ContentPlaceHolder1$txtPre':self.type
                        ,'ctl00$ContentPlaceHolder1$txtNo':awbNumber
                        ,'ctl00$ContentPlaceHolder1$Button2':ur'查询'
                        }

            htmlSource = self.httPost(cargoitranYzrComCn,postData,self.coding.UTF_8,headers)

            rowPanttern = r'<tr.*?>.*?<td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td>.*?</tr>'
            rowMatch = re.findall(rowPanttern,htmlSource,re.DOTALL | re.IGNORECASE)
            
            ATD = ''
            ATA = ''
            PKGS_Count = 0
            PKGS_Current = 0
            dictionaryData = {}
            for x in rowMatch:
                if u'航班已出港' in x[1] and ATD == '':
                    ATD = x[0]
                    PKGS_Count = int(x[2])
                    dictionaryData['MAWB'] = '-'.join((self.type,awbNumber))
                    dictionaryData['ATD'] = ATD

                if u'货物已接收' in x[1]:
                    ATA = x[0]
                    dictionaryData['ATA'] = ATA
                if u'航班已出港' in x[1]:
                     if(PKGS_Count <> 0 and PKGS_Count <> int(x[2])):   #数据的第一行和第二行都有总数,为了确保数据正确过滤
                        PKGS_Current = PKGS_Current + int(x[2])

            if PKGS_Count == PKGS_Current:
                self.InsertByDictionary(self.analyze_table_name,dictionaryData)
                self.InsertByDocument(self.source_table_name,htmlSource)
            else:
                return self.errorStatus
         
        except Exception,e:
            return e

    def init(self):
        self.type = '871'
        self.source_table_name = 'y8'
        self.analyze_table_name = 'y8_analyze'