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
        data = [(row[0], row[1]) for row in rows]
        return data
        # for i in rows: 
        #     return i[0], i[1]
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connect is not None: 
            connect.close()
            print('db connection closed')

if __name__ == "__main__": 
    data = fetch_data()
    with open("marker_data.js", "w") as f: 
        f.write("var marker_data = {};".format(data))

# this method exports data to js file that can be imported to html. this does not fix the issue of too much data on one file. 