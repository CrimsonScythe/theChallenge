from datetime import timedelta
from json import dump
import flask
from flask.json import jsonify
import psycopg2 as pg
import pymongo
from bson.json_util import dumps
from flask import request
import re
import datetime

PASSWORD = 'root'
DBNAME = 'challenge'

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/task1/', methods=['GET'])
def task1():

    client = pymongo.MongoClient(f'mongodb+srv://root:{PASSWORD}@cluster0.ursc6.mongodb.net/{DBNAME}?retryWrites=true&w=majority')
    db = client.challenge
    
    week = request.args.get('week', '')
    sensor_id = request.args.get('sensor_id', '')

    match = re.match(r'[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2} - [0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}', week)
    assert match!=None

    '''clean input a bit removing whitespace between -'''
    week = re.sub(r'\s-\s', '-', week)

    week1 = week.split('-')[0].split(' ')[0]
    time1 = week.split('-')[0].split(' ')[1]
    week2 = week.split('-')[1].split(' ')[0]
    time2 = week.split('-')[1].split(' ')[1]


    # 1,8,15,21 && diff must be 7
    day1 = int(week1.split('/')[0])
    day2 = int(week2.split('/')[0])

    week1 = datetime.datetime(year=int(week1.split('/')[-1]), month=int(week1.split('/')[-2]), day=int(week1.split('/')[-3]), hour=int(time1.split(':')[0]), minute=int(time1.split(':')[1]))
    week2 = datetime.datetime(year=int(week2.split('/')[-1]), month=int(week2.split('/')[-2]), day=int(week2.split('/')[-3]), hour=int(time2.split(':')[0]), minute=int(time2.split(':')[1]))
    
    '''
    we use time delta to easily increment the week
    '''
    week3 = week2 + datetime.timedelta(days=7)

    # print(week1)
    # print(week2)

    '''filter out bad input by making sure that start date is start of week and end date end of week'''
    
    if day1 in [1, 8, 15, 21] and day2-day1==7: 
        print('pass')
    else:
        print('fail')

    dic={'T':'Temperature', 'P':'Pressure', 'F':'Flow-meter', 'E':'Energyconsumption'}
    '''map sensorid to get sensor name, alternative was to put it directly in mongodb or query from postgres'''
    
    sensor_id = sensor_id.replace(sensor_id[0], dic[sensor_id[0]]+' ')

    print(sensor_id)

    pipeline = [
        
        {'$match': {'Date time': {'$gte' : week1, '$lte' : week2} } },
        {'$group': {'_id': None, 'average': {'$avg': '$'+sensor_id}}}
        
    ]

    pipeline1 = [
        
        {'$match': {'Date time': {'$gte' : week2, '$lte' : week3} } },
        {'$group': {'_id': None, 'average': {'$avg': '$'+sensor_id}}}
        
    ]

    week_i_avg = db.sensors.aggregate(pipeline=pipeline)
    week_i1_avg = db.sensors.aggregate(pipeline=pipeline1)


    avg_diff = list(week_i1_avg)[0]['average'] - list(week_i_avg)[0]['average']

    # res = jsonify(list(week_i_avg)[0])
    # print(res)
  
    return {'moving average difference':avg_diff}
 
@app.route('/task2/', methods=['GET'])
def task2():
    
    client = pymongo.MongoClient(f'mongodb+srv://root:{PASSWORD}@cluster0.ursc6.mongodb.net/<dbname>?retryWrites=true&w=majority')
    db = client.challenge
    
    week = request.args.get('week', '')
    sensor_id = request.args.get('sensor_id', '')

    match = re.match(r'[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2} - [0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}', week)
    assert match!=None

    '''clean input a bit removing whitespace between -'''
    week = re.sub(r'\s-\s', '-', week)

    week1 = week.split('-')[0].split(' ')[0]
    time1 = week.split('-')[0].split(' ')[1]
    week2 = week.split('-')[1].split(' ')[0]
    time2 = week.split('-')[1].split(' ')[1]

    week1 = datetime.datetime(year=int(week1.split('/')[-1]), month=int(week1.split('/')[-2]), day=int(week1.split('/')[-3]), hour=int(time1.split(':')[0]), minute=int(time1.split(':')[1]))
    week2 = datetime.datetime(year=int(week2.split('/')[-1]), month=int(week2.split('/')[-2]), day=int(week2.split('/')[-3]), hour=int(time2.split(':')[0]), minute=int(time2.split(':')[1]))

    print(abs((week1-week2).days))

    dic={'T':'Temperature', 'P':'Pressure', 'F':'Flow-meter', 'E':'Energyconsumption'}
    '''map sensorid to get sensor name, alternative was to put it directly in mongodb or query from postgres'''
    
    sensor_id = sensor_id.replace(sensor_id[0], dic[sensor_id[0]]+' ')

    pipeline = [
        
        {'$match': {'Date time': {'$gte' : week1, '$lte' : week2} } },
        {'$group': {'_id': None, 'average': {'$avg': '$'+sensor_id}}}
        
    ]

    res = db.sensors.aggregate(pipeline=pipeline)
    
    return {'moving average':list(res)[0]['average']}

# @app.route('/', methods=['GET'])
# def task3():
#     """
#     docstring
#     """
#     pass

app.run()