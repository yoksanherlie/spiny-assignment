from pytrends.request import TrendReq
from datetime import date, timedelta, datetime
import datetime as dt
import pandas as pd
import pymongo
from pymongo import MongoClient
import argparse

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pull google trends data from keywords in a given day')
    parser.add_argument('date', nargs='?', default=None, help='specific date for google trends data argument, default to yesterday (format: yyyy-mm-dd)')

    args = parser.parse_args()

    if args.date:
        input_date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        input_date = date.today() - dt.timedelta(days=1)

    year = input_date.year
    month = input_date.month
    d = input_date.day

    # google trends api
    pytrends = TrendReq(hl='en-GB', tz=360)

    keywords_csv = pd.read_csv('./top-search-keywords.csv', header=None)
    keywords_csv.columns = ['keywords']

    i = 1
    db = get_db()

    for word in keywords_csv['keywords']:
        print('Getting google trends data for keyword: {}'.format(word))
        hourly_data = pytrends.get_historical_interest(
            [word],
            year_start=year,
            month_start=month,
            day_start=d,
            hour_start=0,
            year_end=year,
            month_end=month,
            day_end=d,
            hour_end=23,
            cat=0,
            geo='GB',
            gprop='',
            sleep=10,
        )
        print('Raw result: {}'.format(hourly_data))
        if not hourly_data.empty:
            hourly_data = hourly_data.drop('isPartial', axis=1)
            hourly_data = hourly_data.loc[hourly_data.index.hour % 4 == 0]

            if db.search_interests.count_documents({'keyword': word}):
                update_dict = {}
                for idx, data in hourly_data.iterrows():
                    update_dict['trends_data.{}'.format(str(idx))] = int(data[word])

                db.search_interests.update_one({'keyword': word}, {
                    '$set': update_dict
                })
            else:
                dicti = {
                    'keyword': word,
                    'trends_data': {}
                }

                for idx, data in hourly_data.iterrows():
                    dicti['trends_data'][str(idx)] = int(data[word])
                
                db.search_interests.insert_one(dicti)
            i += 1

    print("{} keywords' trends pulled".format(i))
