import pandas as pd
import gridstatus 
import plotly.express as px

ISOs = ["CAISO", "PJM", "NYISO", "ISONE"]

class Prices:

    def __init__(self): 
        self.caiso = gridstatus.CAISO()
        self.pjm = gridstatus.PJM()
        self.nyiso = gridstatus.NYISO()
        self.isone = gridstatus.ISONE()
        self.spp = gridstatus.SPP()
        
    def get_CAISO_prices(self): 
        prices = self.caiso.get_lmp(date="today", market="REAL_TIME_5_MIN", locations="ALL")
        chunk_size = 10000
        chunks = [prices[i:i+chunk_size] for i in range(0, len(prices), chunk_size)]
        averages = [chunk["LMP"].mean() for chunk in chunks]
        averages_df = pd.DataFrame({"Chunk": range(1, len(averages) + 1), "Average LMP": averages})
        return averages_df
    
    def get_NYISO_prices(self):
        prices = self.nyiso.get_lmp(date="today", market="REAL_TIME_5_MIN")
        chunk_size = 100
        chunks = [prices[i:i+chunk_size] for i in range(0, len(prices), chunk_size)]
        averages = [chunk["LMP"].mean() for chunk in chunks]
        averages_df = pd.DataFrame({"Chunk": range(1, len(averages) + 1), "Average LMP": averages})
        return averages_df
    
    def get_NEISO_prices(self): 
        prices = self.spp.get_lmp(date="today", market="REAL_TIME_5_MIN", locations="ALL")
        chunk_size = 10000
        chunks = [prices[i:i+chunk_size] for i in range(0, len(prices), chunk_size)]
        averages = [chunk["LMP"].mean() for chunk in chunks]
        averages_df = pd.DataFrame({"Chunk": range(1, len(averages) + 1), "Average LMP": averages})
        return averages_df

# x = Prices()
# z = x.get_NEISO_prices()
# print(z)
    
import plotly.express as px

CAISO_prices = Prices().get_CAISO_prices()
fig = px.line(CAISO_prices, x="Average LMP", y="Chunk", title="CAISO LMP Prices - Today")
fig.show()