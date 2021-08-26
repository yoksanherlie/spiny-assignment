from flask import Flask
import pandas as pd
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    client = MongoClient(
        host='test_db',
        port=27017,
        username='root',
        password='pass',
        authsource='admin'
    )
    db = client['db']
    return db

@app.route('/apis/search_interest/<keyword>')
def api_search_interest(keyword):
    db = get_db()
    data = db.search_interests.find_one({'keyword': keyword})

    if data:
        max_value = max(data['trends_data'].values())
        min_value = min(data['trends_data'].values())
        normalization_result = {}
        for key in data['trends_data'].keys():
            if max_value == 0:
                normalization_result[key] = 0
            else:
                normalization_result[key] = int((data['trends_data'][key] - min_value) / (max_value - min_value) * 100)
        return normalization_result
    return {
        'message': 'Keyword {} not found'.format(keyword)
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')