#coding:utf-8
from helpClass.Base import *

class BR(Base):
    """
    EVA Cargo
    """
    def __init__(self):
        super(BR, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):
        
        try:
            self.httPost('http://www.brcargo.com/EC_WEB/Default.aspx/SetLanguage',"{p_Language: 'ZH-CN' }",self.coding.UTF_8,self.headers) #激活cookie状态,如果未被激活及时发送cookie也不能得到数据
            session = self.getSession()
            cookie = self.dictToString(session.cookies.get_dict())
            self.headers['Cookie'] = cookie

            MAWBSingleQuery = 'http://www.brcargo.com/EC_WEB/TNT/Single_Search.aspx/MAWB_Single_Query'
            MAWBSingleBind = 'http://www.brcargo.com/ec_web/TNT/Single_Search.aspx/MAWB_Single_Bind'

            postData = {'MAWB_CODE': self.type 
                        , 'MAWB_NUMBER': awbNumber
                        , 'CARRIER_CODE': 'BR' }

            seqJson = self.httPost(MAWBSingleQuery,json.dumps(postData),self.coding.UTF_8,self.headers)
            postData = { 'MAWB_CODE': self.type 
                        , 'MAWB_NUMBER': awbNumber
                        , 'SEQ': re.search(r'\d{8,20}',seqJson).group(0)
                        , 'InfoList' : ['TNT/Single_Search','MAWB_Single_Bind','','1','50','1','50','MAWB_Single']}
            
            
            htmlSource = self.httPost(MAWBSingleBind,json.dumps(postData),self.coding.UTF_8,self.headers)
            dataJson = json.loads(json.loads(htmlSource).get('d'))
            tableRowsJson = dataJson.get('TableRows')

            ATD = ''
            ATA = ''
            dictionaryData = {}
            for x in tableRowsJson:
                if ATD == '':
                    ATD = x.get('DEPT_TIME2')
                    if 'Actual'.upper() in ATD.upper():
                        ATD = ' '.join((x.get('TNT_DATE3'),ATD[0:5]))
                        dictionaryData['ATD'] = ATD
                        dictionaryData['MAWB'] = '-'.join((self.type,awbNumber))
                else:
                    ATA = x.get('ARRL_TIME2')
                    if 'Actual'.upper() in ATA.upper():
                        ATA = ' '.join((x.get('TNT_DATE3'),ATA[0:5]))
                        dictionaryData['ATA'] = ATA

            if ATA <> '' and ATD <> '':
                self.InsertByDictionary(self.analyze_table_name,dictionaryData)
                self.Insert(self.source_table_name,htmlSource)
            else:
                return self.errorStatus
    
        except Exception,e:
            return e

    def init(self):
        self.type = '695'
        self.source_table_name = 'br'
        self.analyze_table_name = 'br_analyze'
        self.headers = self.defaultHeaders()

    def defaultHeaders(self):
        self.headers.clear()
        self.headers = {
                        'Accept':' application/json, text/javascript, */*; q=0.01'
                        ,'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
                        ,'Content-Type': 'application/json; charset=UTF-8'
                        ,'DNT':' 1'
                        ,'Connection':'keep-alive'
                        ,'Referer':' http://www.brcargo.com/ec_web/?Parm2=MenuID_191&Parm3='
                        #,'Cookie': 'ASP.NET_SessionId=n4uwcf55wddrum55ghym0va2; CargoEC=1329791754.20480.0000;'
                        }
        return self.headers

    def dictToString(self,dict):
        cookieString = ''
        for key, value in dict.iteritems():
            cookieString+= '{key}={value}; '.format(key=key,value=value)
        return cookieString