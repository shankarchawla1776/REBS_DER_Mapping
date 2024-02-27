import psycopg2 
import json 

from config import config

def fetch_data(wind=None): 
    connect = None 
    try:
        params = config()
        connect = psycopg2.connect(**params)
        cursor = connect.cursor()
        if wind:
            cursor.execute('SELECT ylat, xlong FROM "USWTDB"')
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
    data = fetch_data(wind=True)
    with open("data.json", "w") as f: 
        json.dump(data, f)




    # with open("marker_data.js", "w") as f: 
    #     f.write("var marker_data = {};".format(data))

# this method exports data to js file that can be imported to html. this does not fix the issue of too much data on one file. 