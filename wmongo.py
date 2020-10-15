from os import spawnl
import pickle
import pymongo
import datetime

PASSWORD = 'root'

'''
load pickle file
'''

with open('sensor_values.pickle', 'rb') as file:
        df = pickle.load(file)

print(df)

'''
replace str date time values with datetime datatype
I think this would make querying easier
'''

for i in range(len(df['Date time'])):
        temp_date = df['Date time'][i].split(' ')[0]
        temp_time = df['Date time'][i].split(' ')[1]
        df['Date time'][i] = datetime.datetime(year=int(temp_date.split('/')[-1]), month=int(temp_date.split('/')[-2]), day=int(temp_date.split('/')[-3]), hour=int(temp_time.split(':')[-2]), minute=int(temp_time.split(':')[-1]))

print(df['Date time'])

'''
Connect to db and populate
'''

client = pymongo.MongoClient(f'mongodb+srv://root:{PASSWORD}@cluster0.ursc6.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = client.challenge

'''
We use the convenient to_dict() function with records as return type for easy insertion
'''
result = db.sensors.insert_many(df.to_dict('records'))
