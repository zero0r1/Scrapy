from helpClass.Base import *
from __builtin__ import str, int

class csCargoCapture(Base):
    def __init__(self):
        super(csCargoCapture, self).__init__()
        self.init()

    def getHtmlData(self,awbNumber):
        htmlSource = ''
        try:
            self.outputLog('%s-%s start...' % (self.type,awbNumber))

            headers = self.defaultHeaders()
            urlCsCargoTracking = 'http://tang.cs-air.com/WebFace/Tang.WebFace.Cargo/AgentAwbBrower.aspx?AwbPrefix=784&AwbNo={AwbNo}&menuID=1'.format(AwbNo=awbNumber)
            htmlSource = self.httpGet(urlCsCargoTracking,'UTF-8',headers)
            keyPattern = r'__VIEWSTATE" value="(.*?)"'
            keyMatch = re.search(keyPattern, htmlSource,re.DOTALL | re.MULTILINE)
            key = keyMatch.group(1)

            aaCargoPostData = {'__VIEWSTATE':'{__VIEWSTATE}'.format(__VIEWSTATE=key)
            ,'ctl00$ContentPlaceHolder1$txtPrefix':'{Prefix}'.format(Prefix=self.type)
            ,'ctl00$ContentPlaceHolder1$txtNo':'{No}'.format(No=awbNumber)
            ,'ctl00$ContentPlaceHolder1$cbIsInter':'on'
            ,'ctl00$ContentPlaceHolder1$btnBrow':'查看'
            ,'ctl00$ContentPlaceHolder1$hfCurrentArea':'(当地时间)'
            ,'ctl00$lancode':'zh-cn'}

            self.outputLog('request web.')
            htmlSource = self.httPost(urlCsCargoTracking,aaCargoPostData,'UTF-8',headers)

            tablePattern = r'<table.*?id="ctl00_ContentPlaceHolder1_gvCargoState.*?>(.*?)</table>'
            tableMatch = re.search(tablePattern, htmlSource,re.DOTALL | re.MULTILINE)

            rowPattern = r'<td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td>'
            rowMatch = re.findall(rowPattern,tableMatch.group(1),re.DOTALL | re.MULTILINE)
            
            cargoCountNumber = int(rowMatch[0][4].strip())
            cargoCurrentNumber = 0
            atd = ''
            self.outputLog('analyze data...')
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
                self.InsertByDictionary('cs_cargo_analyze',dictionaryData)
                self.outputLog('save data to the data base')
                self.InsertByDocument('cs_cargo',htmlSource)
                self.outputLog('{type}-{awbNumber} done.'.format(type=self.type,awbNumber=awbNumber))
            else:
                return self.errorStatus     #当返回数据的时候外部调用不更新状态,等待下一次的抓取
            
        except Exception,e:
            self.outputLog('getHtmlData {0}'.format(e))
            return self.errorStatus

    def init(self):
        self.type = '784'