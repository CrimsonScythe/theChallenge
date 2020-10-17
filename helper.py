from abc import ABC, abstractmethod
import re
import datetime

'''
Checks week input and maps sensor id to sensornames.
'''

class ParserHelper(ABC):
    @abstractmethod
    def parseWeek(week):

        match = re.match(r'[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2} - [0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}', week)
        # assert match!=None

        if (match==None):
            return None

        '''clean input a bit removing whitespace between -'''
        week = re.sub(r'\s-\s', '-', week)

        week1 = week.split('-')[0].split(' ')[0]
        time1 = week.split('-')[0].split(' ')[1]
        week2 = week.split('-')[1].split(' ')[0]
        time2 = week.split('-')[1].split(' ')[1]


        # 1,8,15,21 && diff must be 7
        day1 = int(week1.split('/')[0])
        day2 = int(week2.split('/')[0])

        '''
        to catch invalid input like if day==0
        '''
        try:
            week1 = datetime.datetime(year=int(week1.split('/')[-1]), month=int(week1.split('/')[-2]), day=int(week1.split('/')[-3]), hour=int(time1.split(':')[0]), minute=int(time1.split(':')[1]))
            week2 = datetime.datetime(year=int(week2.split('/')[-1]), month=int(week2.split('/')[-2]), day=int(week2.split('/')[-3]), hour=int(time2.split(':')[0]), minute=int(time2.split(':')[1]))
        
        except(ValueError) as err:
            return None

        return week1, week2, day1, day2
    
    def parseSensor(sensor_id):

        '''map sensorid to get sensor name, alternative was to put it directly in mongodb or query from postgres'''

        dic={'T':'Temperature', 'P':'Pressure', 'F':'Flow-meter', 'E':'Energyconsumption'}
        ret_sensor=''
        try:
            ret_sensor = sensor_id.replace(sensor_id[0], dic[sensor_id[0]]+' ', )
        except(KeyError) as err:
            return None

        

        return ret_sensor