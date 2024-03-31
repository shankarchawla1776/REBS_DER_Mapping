import gridstatus as gs 
import pandas as pd 

class write_daily_prices: 

    def get_prices(self, isos=[]): 
        for i in isos: 
                call_dict = {"CAISO": gs.CAISO(), "NYISO": gs.NYISO(), "PJM": gs.PJM(), "MISO": gs.MISO(), "ISONE": gs.ISONE()}
                y = call_dict[i]
                prices = y.get_lmp(date="today", market='REAL_TIME_5_MIN', locations='all')
        return pd.DataFrame(prices)
    
call = write_daily_prices()
df = call.get_prices(['CAISO'])
df.to_csv('daily_pricing/caiso_prices.csv')