import psycopg2 

from config import config 

def fetch_data(): 
    connect = None 
    try:
        params = config()
        connect = psycopg2.connect(**params)
        cursor = connect.cursor()
    
        cursor.execute('SELECT xlong, ylat FROM "USWTDB"')
        rows = cursor.fetchall()
        for i in rows: 
            print(i[0], i[1])
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connect is not None: 
            connect.close()
            print('db connection closed')

if __name__ == "__main__": 
    fetch_data()