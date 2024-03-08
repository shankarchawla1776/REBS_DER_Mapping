import psycopg2 
from data_fetching.config import config

class DataFetcher: 

    def __init__(self): 
        self.connection = None
    
    def connect(self):
        try: 
            params = config()
            self.connection = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
    def fetch_data(self, data=None): 
        queries = {
            "wind_turbines": 'SELECT ylat, xlong FROM "USWTDB"',
            "distributed_solar": 'SELECT latitude, longitude FROM "Distributed_Solar"'
        }
        if data not in queries:
            raise ValueError("Data does not exist")
        try: 
            if self.connection is None:
                self.connect()
            # self.connect = psycopg2.connect(**config())
            cursor = self.connection.cursor()
            cursor.execute(queries[data])
            rows = cursor.fetchall()
            data = [(row[0], row[1]) for row in rows]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return data
    
    def close(self): 
        if self.connection is not None: 
            self.connection.close()
            print('db connection closed')

if __name__ == "__main__": 
    data_fetcher = DataFetcher()
    data_fetcher.connect()
    wind_data = data_fetcher.fetch_data(data="wind_turbines")

