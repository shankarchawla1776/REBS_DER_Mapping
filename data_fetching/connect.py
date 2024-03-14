import psycopg2
from data_fetching.config import config

"""
Server no longer active
"""

def connection(): 
    connect = None 
    try:
        params = config()
        connect = psycopg2.connect(**params)
        cursor = connect.cursor()
        cursor.execute('SELECT version()')
        version = cursor.fetchone()
        print(version)
        cursor.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally: 
        if connect is not None: 
            connect.close()
            print('db connection closed')

if __name__ == "__main__": 
    connection()

