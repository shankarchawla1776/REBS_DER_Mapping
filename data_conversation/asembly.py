import pandas as pd 
from data_fetching.fetch_data import DataFetcher

"""
Fetches data from a NOT public Postgres database to assemble a comprehensive dataframe 
of latitude and longitude coordinates and a label for the type of DER. This dataframe 
can be found in the PUBLIC s3 bucket. 

The full coordinate data can be accessed with the s3 URI at 
DER_data/full_coordinates.csv
"""

class dfAssembly:

    def __init__(self): 
        self.data_fetching = DataFetcher()
        self.wind_turbines = self.data_fetching.fetch_data(data="wind_turbines") 
        self.distributed_solar = self.data_fetching.fetch_data(data="distributed_solar")
        self.utility_solar = self.data_fetching.fetch_data(data="utility_solar")

    def assemble(self): 
        df = pd.DataFrame(self.wind_turbines, columns=["latitude", "longitude"])
        df["type"] = "wind_turbines"
        
        df2 = pd.DataFrame(self.distributed_solar, columns=["latitude", "longitude"])
        df2["type"] = "distributed_solar"
        
        df3 = pd.DataFrame(self.utility_solar, columns=["latitude", "longitude"])
        df3["type"] = "utility_solar"
        
        full = pd.concat([df, df2, df3], ignore_index=True)
        full.to_csv("full_coordinates.csv", index=False)
    

assembly_instance = dfAssembly()
exc = assembly_instance.assemble()
