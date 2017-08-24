from helpClass.Base import *
from __builtin__ import str

class aaCargoCapture(Base):
    def __init__(self):
        super(aaCargoCapture, self).__init__()
        self.init()

    def getHtmlData(self,awbNumber):

        try:
            self.outputLog('{type}-{awbNumber} start...'.format(type=self.type,awbNumber=awbNumber))

            headers = self.defaultHeaders()
            urlAACargoTracking = 'https://www.aacargo.com/AACargo/tracking'
            aaCargoPostData = {'trackingPath':'track10'
    ,'airwayBills[0].awbCode':'001'
    ,'airwayBills[0].awbNumber':'{awbNumber}'.format(awbNumber=awbNumber)
    ,'airwayBills[1].awbCode':''
    ,'airwayBills[1].awbNumber':''
    ,'airwayBills[2].awbCode':''
    ,'airwayBills[2].awbNumber':''
    ,'airwayBills[3].awbCode':''
    ,'airwayBills[3].awbNumber':''
    ,'airwayBills[4].awbCode':''
    ,'airwayBills[4].awbNumber':''
    ,'airwayBills[5].awbCode':''
    ,'airwayBills[5].awbNumber':''
    ,'airwayBills[6].awbCode':''
    ,'airwayBills[6].awbNumber':''
    ,'airwayBills[7].awbCode':''
    ,'airwayBills[7].awbNumber':''
    ,'airwayBills[8].awbCode':''
    ,'airwayBills[8].awbNumber':''
    ,'airwayBills[9].awbCode':''
    ,'airwayBills[9].awbNumber':''
    ,'track10Search':'Track'}
       
            self.outputLog('request web.')
            htmlSource = self.httPost(urlAACargoTracking,aaCargoPostData,'ISO-8859-1',headers)

            self.outputLog('analyze web data and find number')
            pattern = r'<!-- ACTION LINKS -->.*<input\stype="hidden"\svalue="(\d{8})"'
            match = re.search(pattern, htmlSource,re.DOTALL)

            firstOneMawbNO = match.group(1)

            self.outputLog('request aacargo json data')
            urlMasterAirWayBillDetails = 'https://www.aacargo.com/AACargo/tracking/masterAirWayBillDetails?airwayBillId=<airwayBillId>'.replace('<airwayBillId>',firstOneMawbNO)
            masterAirWayBillDetailsSource = self.httpGet(urlMasterAirWayBillDetails,'ISO-8859-1',headers)


            convertJson = json.loads(masterAirWayBillDetailsSource)
            airWayBillTrackingHistoryDtos = convertJson.get('airWayBillTrackingHistoryDtos')
            bookedFlightDetailsList = convertJson.get('bookedFlightDetailsList')
            
            currentFlightNumber = 0
            countFlightNumber = 0
            ata = ''
            dictionaryData = {}
            self.outputLog('analyze data...')
            for node in airWayBillTrackingHistoryDtos:
               if 'Flight Arrived' in node.get('status') and ata == '':     #由于最新的数据在最顶端,所以第一次进来就是获取最新数据
                   dictionaryData['MAWB_NO'] = '-'.join((self.type,awbNumber))
                   dictionaryData['ATA'] = ' at '.join((node.get('gateInDate'),node.get('gateInTime')))
                   ata = dictionaryData['ATA']
                   currentFlightNumber = currentFlightNumber + 1    #每一次都要计算飞机架次
               elif 'Flight Arrived' in node.get('status'):
                    currentFlightNumber = currentFlightNumber + 1   #每一次都要计算飞机架次

               if 'Flight Departed' in node.get('status'):
                   dictionaryData['ATD'] = ' at '.join((node.get('departedGateDate'),node.get('departedGateTime')))
                   

            for node in bookedFlightDetailsList:
                if str(node.get('airlineIATACode')).strip().upper() == 'AA':
                    countFlightNumber = countFlightNumber + 1

            if countFlightNumber == currentFlightNumber:
                self.InsertByDictionary('aa_cargo_analyze',dictionaryData)
                self.outputLog('save data to the data base')
                self.Insert('aa_cargo',masterAirWayBillDetailsSource)
                self.outputLog('{type}-{awbNumber} done.'.format(type=self.type,awbNumber=awbNumber))
            else:
                return self.errorStatus     #当返回数据的时候外部调用不更新状态,等待下一次的抓取
        except Exception,e:
            self.outputLog('getHtmlData %s' % e)
            return self.errorStatus

    def init(self):
        self.type = '001'