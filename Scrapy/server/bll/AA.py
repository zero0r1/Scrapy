#coding:utf-8
from helpClass.Base import *

class AA(Base):
    """
    American Airlines
    """
    def __init__(self):
        
        super(AA, self).__init__()
        self.init()

    @opinfo
    def getHtmlData(self,awbNumber):

        try:
            headers = self.defaultHeaders()
            urlAACargoTracking = 'https://www.aacargo.com/AACargo/tracking'
            aaCargoPostData = {'trackingPath':'track10'
                                ,'airwayBills[0].awbCode':'001'
                                ,'airwayBills[0].awbNumber':awbNumber
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
       
            
            htmlSource = self.httPost(urlAACargoTracking,aaCargoPostData,self.coding.ISO_8859_1,headers)
            pattern = r'<!--\s*ACTION\s*LINKS\s*-->.*<input\s*type="hidden"\s*value="(\d{8})"'
            match = re.search(pattern, htmlSource,re.DOTALL)

            firstOneMawbNO = match.group(1)

            urlMasterAirWayBillDetails = 'https://www.aacargo.com/AACargo/tracking/masterAirWayBillDetails?airwayBillId=<airwayBillId>'.replace('<airwayBillId>',firstOneMawbNO)
            masterAirWayBillDetailsSource = self.httpGet(urlMasterAirWayBillDetails,self.coding.ISO_8859_1,headers)


            convertJson = json.loads(masterAirWayBillDetailsSource)
            airWayBillTrackingHistoryDtos = convertJson.get('airWayBillTrackingHistoryDtos')
            bookedFlightDetailsList = convertJson.get('bookedFlightDetailsList')
            
            currentFlightNumber = 0
            countFlightNumber = 0
            ATA = ''
            dictionaryData = {}
            for node in airWayBillTrackingHistoryDtos:
               if 'Flight Arrived'.upper() in node.get('status').upper() and ATA == '':     #由于最新的数据在最顶端,所以第一次进来就是获取最新数据
                   dictionaryData['MAWB_NO'] = '-'.join((self.type,awbNumber))
                   dictionaryData['ATA'] = ' at '.join((node.get('gateInDate'),node.get('gateInTime')))
                   ATA = dictionaryData['ATA']
                   currentFlightNumber = currentFlightNumber + 1    #每一次都要计算飞机架次
               elif 'Flight Arrived'.upper() in node.get('status').upper():
                    currentFlightNumber = currentFlightNumber + 1   #每一次都要计算飞机架次

               if 'Flight Departed'.upper() in node.get('status').upper():
                   dictionaryData['ATD'] = ' at '.join((node.get('departedGateDate'),node.get('departedGateTime')))
                   

            for node in bookedFlightDetailsList:
                if str(node.get('airlineIATACode')).strip().upper() == 'AA'.upper():
                    countFlightNumber = countFlightNumber + 1

            if countFlightNumber == currentFlightNumber:
                self.InsertByDictionary(self.analyze_table_name,dictionaryData)
                self.Insert(self.source_table_name,masterAirWayBillDetailsSource)
            else:
                return self.errorStatus     #当返回数据的时候外部调用不更新状态,等待下一次的抓取
        except Exception,e:
            return e

    def init(self):
        self.type = '001'
        self.source_table_name = 'aa'
        self.analyze_table_name = 'aa_analyze'