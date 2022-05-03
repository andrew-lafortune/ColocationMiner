import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import time
import ast

day_list = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def avg_popularity(row):
    out = {}
    for day, count in ast.literal_eval(row['popularity_by_day']).items():
        start = date.fromtimestamp(row['date_range_start'])
        end = date.fromtimestamp(row['date_range_end'])
        out[day] = count / np.busday_count(start,end,day[0:3])
    return out

def date_list(row):
    return [date.fromtimestamp(row['date_range_start']) + timedelta(days=i) for i in range(len(ast.literal_eval(row['visits_by_day'])))]

def expected_by_day(row):
    return row['avg_popularity_by_day'][day_list[row['date'].weekday()]]

def clean(fin, fout, start_date=None, end_date=None):
    data = pd.read_csv('raw/' + fin)

    if(start_date and end_date):
        start_date = datetime.strptime(start_date, '%Y/%m/%d').date()
        end_date = datetime.strptime(end_date, '%Y/%m/%d').date()
    elif(start_date):
        start_date = date.strftime(start_date, '%Y/%m/%d').date()
        end_date = date.today()
    else:
        start_date = date.fromtimestamp(0)
        end_date = date.today()

    unixstart = time.mktime(start_date.timetuple())
    unixend = time.mktime(end_date.timetuple())

    window = data[(data['date_range_start'] < unixend) & (data['date_range_end'] > unixstart)]
    window['avg_popularity_by_day'] = window.apply(avg_popularity, axis=1)
    window['date'] = window.apply(date_list,axis=1)
    window['visits'] = window['visits_by_day'].apply(lambda x: ast.literal_eval(x))
    window = window.explode(['date', 'visits'])
    window['expected_visits'] = window.apply(expected_by_day, axis=1)

    cleaned = window[['safegraph_place_id','location_name','brands','top_category','sub_category','date','visits','expected_visits','latitude','longitude']]
    cleaned.to_csv('data/'+fout, index=False)