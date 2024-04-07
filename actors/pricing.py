import pandas as pd
import gridstatus 
import plotly.express as px

ISOs = ["CAISO", "PJM", "NYISO", "ISONE"]

class Prices:

    def __init__(self): 
        pass
        
    def get_CAISO_prices(self):
        prices_file = "daily_pricing/nyiso_prices.csv"
        chunks = pd.read_csv(prices_file, chunksize=10000)
        averages = [chunk["LMP"].mean() for chunk in chunks]
        averages_df = pd.DataFrame({"Chunk": range(1, len(averages) + 1), "Average LMP": averages})
        return averages_df

    def get_NYISO_prices(self):
        prices_file = "daily_pricing/nyiso_prices.csv"
        chunks = pd.read_csv(prices_file, chunksize=10000)
        averages = [chunk["LMP"].mean() for chunk in chunks]
        averages_df = pd.DataFrame({"Chunk": range(1, len(averages) + 1), "Average LMP": averages})
        return averages_df

    def get_MISO_prices(self):
        prices_file = "daily_pricing/nyiso_prices.csv"
        chunks = pd.read_csv(prices_file, chunksize=10000)
        averages = [chunk["LMP"].mean() for chunk in chunks]
        averages_df = pd.DataFrame({"Chunk": range(1, len(averages) + 1), "Average LMP": averages})
        return averages_df


