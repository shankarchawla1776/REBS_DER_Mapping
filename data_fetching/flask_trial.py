from flask import Flask, jsonify, render_template
import psycopg2
from data_fetching.config import config

app = Flask(__name__)

def fetch_data(page=1, per_page=100):
    connect = None
    try:
        params = config()
        connect = psycopg2.connect(**params)
        cursor = connect.cursor()

        offset = (page - 1) * per_page
        cursor.execute('SELECT xlong, ylat FROM "USWTDB" LIMIT %s OFFSET %s', (per_page, offset))
        rows = cursor.fetchall()
        data = [[row[0], row[1]] for row in rows]
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connect is not None:
            connect.close()
            print('db connection closed')


@app.route('/')
def map():
    data = fetch_data()
    return render_template('map.html, data=data')

if __name__ == "__main__":
    app.run(debug=True)