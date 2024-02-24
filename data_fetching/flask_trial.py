from flask import Flask, request, jsonify
from data_fetching.fetch_data import fetch_data

app = Flask(__name__)


all_data = fetch_data()

@app.route('/data')
def get_data():
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=1000, type=int)

    start_index = (page - 1) * size
    end_index = min(start_index + size, len(all_data))

    paginated_data = all_data[start_index:end_index]

    return jsonify(paginated_data)

if __name__ == '__main__':
    app.run(debug=True)
