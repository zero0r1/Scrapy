from helpClass.Base import *

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

            tablePattern = r''
            tableMatch = re.findall(tablePattern, htmlSource,re.DOTALL | re.MULTILINE)


        except Exception,e:
            self.outputLog('getHtmlData {0}'.format(e))
            return self.errorStatus

    def init(self):
        self.type = '784'