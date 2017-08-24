#coding:utf-8
from helpClass.Base import *

class CZ(Base):
    """
    中国南方航空
    """
    def __init__(self):
        super(CZ, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):
        htmlSource = ''
        try:

            headers = self.defaultHeaders()
            urlCsCargoTracking = 'http://tang.cs-air.com/WebFace/Tang.WebFace.Cargo/AgentAwbBrower.aspx?AwbPrefix=784&AwbNo={AwbNo}&menuID=1'.format(AwbNo=awbNumber)
            htmlSource = self.httpGet(urlCsCargoTracking,self.coding.UTF_8,headers)
            keyPattern = r'__VIEWSTATE" value="(.*?)"'
            keyMatch = re.search(keyPattern, htmlSource,re.DOTALL | re.IGNORECASE)
            key = keyMatch.group(1)

            aaCargoPostData = {'__VIEWSTATE':key
            ,'ctl00$ContentPlaceHolder1$txtPrefix':self.type
            ,'ctl00$ContentPlaceHolder1$txtNo':awbNumber
            ,'ctl00$ContentPlaceHolder1$cbIsInter':'on'
            ,'ctl00$ContentPlaceHolder1$btnBrow':'查看'
            ,'ctl00$ContentPlaceHolder1$hfCurrentArea':'(当地时间)'
            ,'ctl00$lancode':'zh-cn'}

            
            htmlSource = self.httPost(urlCsCargoTracking,aaCargoPostData,self.coding.UTF_8,headers)

            tablePattern = r'<table.*?id="ctl00_ContentPlaceHolder1_gvCargoState.*?>(.*?)</table>'
            tableMatch = re.search(tablePattern, htmlSource,re.DOTALL | re.IGNORECASE)

            rowPattern = r'<td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td>'
            rowMatch = re.findall(rowPattern,tableMatch.group(1),re.DOTALL | re.IGNORECASE)
            
            cargoCountNumber = int(rowMatch[0][4].strip())
            cargoCurrentNumber = 0
            atd = ''
            dictionaryData = {}
            for x in rowMatch:
                if u'航班已起飞' in x[3] and atd == '':    #货物状态
                    ata = x[0].strip()
                    dictionaryData['ATD'] = ata
                    dictionaryData['MAWB_NO'] = '-'.join((self.type,awbNumber))

                if u'货物已装机' in x[3]:
                    cargoCurrentNumber+=int(x[4].strip())

                if u'航班已到达' in x[3]:
                    dictionaryData['ATA'] = x[0].strip()
            
            if cargoCountNumber == cargoCurrentNumber:
                self.outputLog('save data to the data base')
                self.InsertByDictionary(self.source_table_name,dictionaryData)
                self.InsertByDocument(self.analyze_table_name,htmlSource)
            else:
                return self.errorStatus     #当返回数据的时候外部调用不更新状态,等待下一次的抓取
            
        except Exception,e:
            return e

    def init(self):
        self.type = '784'
        self.source_table_name = 'cz'
        self.analyze_table_name = 'cz_analyze'