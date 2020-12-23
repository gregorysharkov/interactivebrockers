from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData
from ContractSamples import ContractSamples

from datetime import datetime


class TestApp(EWrapper,EClient):

    def __init__(self):
        EClient.__init__(self, self)

    
    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    
    def historicalData(self, reqId:int, bar: BarData):
        print(bar)
        with open(".data/EurGbpFx.txt", mode="a+") as f:
            f.write(bar)
            f.close()
    
    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)


def main():
    #queryTime = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime("%Y%m%d %H:%M:%S")

    app = TestApp()
    app.connect("127.0.0.1", 7497, 0)

    app.reqHistoricalData(
        1, 
        ContractSamples.EurGbpFx(), 
        "", 
        "1 D", 
        "1 min", 
        "MIDPOINT", 
        1, 
        1, 
        False,
        []
    )
    
    app.run()

if __name__ == '__main__':
    main()