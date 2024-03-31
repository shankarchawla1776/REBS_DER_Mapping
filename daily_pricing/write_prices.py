import gridstatus as gs 
import pandas as pd 

class write_daily_prices: 

    def get_prices(self): 
        caiso = gs.CAISO()
        prices = caiso.get_lmp(date="today", market='REAL_TIME_5_MIN', locations='all')
        return pd.DataFrame(prices)
    
call = write_daily_prices()
df = call.get_prices()
df.to_csv('daily_prices.csv')
