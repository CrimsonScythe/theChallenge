from datetime import timedelta
from helper import ParserHelper
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

    parsedWeek = ParserHelper.parseWeek(week=week)

    if parsedWeek==None:
        return 'Error. Week range must be given in the format: \'dd/mm/yyyy hh:mm - dd/mm/yyyy hh:mm\''

    week1, week2, day1, day2 = parsedWeek

    ''' we use time delta to easily increment the week'''
    week3 = week2 + datetime.timedelta(days=7)

    '''filter out bad input by making sure that start date is start of week and end date end of week'''
    
    if (day1 in [1, 8, 15, 21] and day2-day1==7)==False: 
        return 'Error. day of first week must be a starting week (one of 1, 8, 15, 21)'

    
    sensor_id = ParserHelper.parseSensor(sensor_id=sensor_id)
    if sensor_id==None:
        return 'Error. sensor_id not valid'

    print(sensor_id)

    pipeline = [
        
        {'$match': {'Date time': {'$gte' : week1, '$lte' : week2} } },
        {'$group': {'_id': None, 'average': {'$avg': '$'+sensor_id}}}
        
    ]

    pipeline1 = [
        
        {'$match': {'Date time': {'$gte' : week2, '$lte' : week3} } },
        {'$group': {'_id': None, 'average': {'$avg': '$'+sensor_id}}}
        
    ]

    week_i_avg = list(db.sensors.aggregate(pipeline=pipeline))
    week_i1_avg = list(db.sensors.aggregate(pipeline=pipeline1))

    
    if (week_i_avg)[0]['average']==None or (week_i1_avg)[0]['average']==None:
        return 'Error. No entries found for the week and sensor_id'

  
    avg_diff = (week_i1_avg)[0]['average'] - (week_i_avg)[0]['average']
    

    return {'moving average difference':avg_diff}
 
@app.route('/task2/', methods=['GET'])
def task2():
    
    client = pymongo.MongoClient(f'mongodb+srv://root:{PASSWORD}@cluster0.ursc6.mongodb.net/{DBNAME}?retryWrites=true&w=majority')
    db = client.challenge
    
    week = request.args.get('week', '')
    sensor_id = request.args.get('sensor_id', '')

    parsedWeek = ParserHelper.parseWeek(week=week)
    if parsedWeek==None:
        return 'Error. Week range must be given in the format: \'dd/mm/yyyy hh:mm - dd/mm/yyyy hh:mm\''
    week1, week2, _, _ = parsedWeek

    sensor_id = ParserHelper.parseSensor(sensor_id=sensor_id)
    if sensor_id==None:
        return 'Error. sensor_id not valid'



    pipeline = [
        
        {'$match': {'Date time': {'$gte' : week1, '$lte' : week2} } },
        {'$group': {'_id': None, 'average': {'$avg': '$'+sensor_id}}}
        
    ]

    res = list(db.sensors.aggregate(pipeline=pipeline))
    
    if (res)[0]['average'] == None:
        return 'Error. No entries found for the week and sensor_id'

    return {'moving average':res[0]['average']}

@app.route('/task3/', methods=['GET'])
def task3():


    machine_id = request.args.get('machine_id', '')

    connection = pg.connect(dbname='challenge', user='postgres', password='root')
    cur = connection.cursor()

    sensor_query = f''' SELECT (sensors.sensor_id, sensors.sensor_name) FROM sensors WHERE sensors.machine_id='{machine_id}'; '''
    cur.execute(sensor_query)
    sensor_info = cur

    cur = connection.cursor()

    machine_query = f''' SELECT (machines.status, machines.location_id) FROM machines WHERE machines.machine_id='{machine_id}'; '''
    cur.execute(machine_query)
    machine_info = cur      

    machine_info = machine_info.fetchall()
    sensor_info = sensor_info.fetchall() 

    if len(machine_info)==0:
        return 'Error. No machines found for the given ID.'

    machine_info = re.sub(r'\(*\)*', '', machine_info[0][0])

    dic = {}

    lst = []
    
    for i in range(len(sensor_info)):
        print(sensor_info[i][0])
        sensor_temp = re.sub(r'\(*\)*', '', sensor_info[i][0])
        print(sensor_temp)
        lst.append([sensor_temp.split(',')[0], sensor_temp.split(',')[1].replace('"', '')]) 

    dic['machine_id'] = machine_id
    dic['sensors'] = lst
    dic['status'] = machine_info.split(',')[0]
    dic['location'] = machine_info.split(',')[1]

    cur.close()

    return dic

app.run()