from helpClass.Base import *
from __builtin__ import str, int

class airChinaCargoCapture(Base):
    def __init__(self):
        super(airChinaCargoCapture, self).__init__()
        self.init()

    def getHtmlData(self,awbNumber):

        try:
            self.outputLog('%s-%s start...' % (self.type,awbNumber))

            headers = self.defaultHeaders()
            urlAirChinaCargoTracking = 'http://www.airchinacargo.com/search_order.php'
            aaCargoPostData = {'trackingPath':'track10'
    ,'orders10':'{0}'.format(self.type)
    ,'orders0':'{0}'.format(awbNumber)
    ,'orders11':''
    ,'orders1[':''
    ,'orders12':''
    ,'orders2':''
    ,'orders13':''
    ,'orders3':''
    ,'orders14':''
    ,'orders4':''
    ,'orders9':''
    ,'section':'0-0001-0003-0081'
    ,'x[6]':'0'
    ,'y[6]':'0'}
       
            self.outputLog('request web.')
            htmlSource = self.httPost(urlAirChinaCargoTracking,aaCargoPostData,'UTF-8',headers)
            pattern = r'<tr.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>'
            match = re.findall(pattern, htmlSource,re.DOTALL | re.MULTILINE)

            rcsType = 'RCS'
            rcfType = 'RCF'
            rcsNumber = 0
            rcfNumber = 0

            self.outputLog('analyze data...')
            dictionaryData = {}
            for x in match:
                if rcsType in x[0]:     #状态名称format by RCS(货物收运)
                    rcsNumber = int(x[2].strip())
                    dictionaryData['ATD'] = match[1][5].strip()
                    dictionaryData['MAWB_NO'] = '-'.join((self.type,awbNumber))
                if rcfType in x[0]:
                    rcfNumber = rcfNumber + int(x[2].strip())

            if rcsNumber == rcfNumber and rcsNumber != 0 and rcfNumber != 0:   #当两数相等时候ATD时间出现
                dictionaryData['ATA'] = x[5].strip()
                self.outputLog('save data to the data base')
                self.InsertByDictionary('air_china_cargo_analyze',dictionaryData)
                self.InsertByDocument('air_china_cargo',htmlSource)
                self.outputLog('{type}-{awbNumber} done.'.format(type=self.type,awbNumber=awbNumber))
            else:
                return self.errorStatus

        except Exception,e:
            self.outputLog('getHtmlData {0}'.format(e))
            return self.errorStatus

    def init(self):
        self.type = '999'