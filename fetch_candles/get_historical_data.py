from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData
from ContractSamples import ContractSamples

from datetime import datetime


class TestApp(EWrapper,EClient):

    def __init__(self):
        EClient.__init__(self, self)
        self.filename = "fetch_candles\\data\\EurGbpFx.txt"
        #clear the contents of the file
        f = open(self.filename, 'r+')
        f.truncate(0)
        f.close()
    
    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    
    def historicalData(self, reqId:int, bar: BarData):
        print(str(bar))
        with open(self.filename, mode="a") as f:
            f.write(str(bar)+"\n")
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
        "10 D", 
        "1 min", 
        "MIDPOINT", 
        0, 
        1, 
        False,
        []
    )
    
    app.run()

if __name__ == '__main__':
    main()