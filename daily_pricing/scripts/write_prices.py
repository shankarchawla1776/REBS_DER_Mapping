import gridstatus as gs 
import pandas as pd 

class write_daily_prices: 

    def __init__(self): 

        self.CAISO = gs.CAISO() 
        self.NYISO = gs.NYISO()
        self.MISO = gs.MISO()
    
    def get_data(self, isos=[]): 
        for i in isos: 
            if i == "CAISO": 
                prices = self.CAISO.get_lmp(date="today", market="REAL_TIME_5_MIN", locations="ALL")
                prices.to_csv("daily_pricing/caiso_prices.csv")
            elif i == "NYISO":
                prices = self.NYISO.get_lmp(date="today", market="REAL_TIME_5_MIN", locations="ALL")
                prices.to_csv("daily_pricing/nyiso_prices.csv")
            elif i == "MISO":
                prices = self.MISO.get_lmp(date="today", market="REAL_TIME_5_MIN", locations="ALL")
                prices.to_csv("daily_pricing/miso_prices.csv")

call = write_daily_prices()
prices = call.get_data(isos=["NYISO"])
