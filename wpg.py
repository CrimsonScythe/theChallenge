import psycopg2 as pg
import pandas as pd
import psycopg2.extras as pge
'''
Creates database
'''
def init_db(name='challenge'):
    try:
        cur = connection.cursor()
        cmd = f''' CREATE database {name} '''
        cur.execute(cmd)
        cur.close()
        connection.commit()
    except(Exception, pg.Error) as error:
        print('Error creating database', error)


'''
Creates database tables
'''
def init_tables():

    try:
        '''
        create new connection to connect to newly created db
        '''
        connection = pg.connect(dbname='challenge', user='postgres', password='root')
        cur = connection.cursor()
        
        tables = (
            """
            CREATE TABLE sensors (
                sensor_id VARCHAR(30) PRIMARY KEY,
                sensor_name VARCHAR,
                machine_id VARCHAR(30)
            )
            """,
            """
            CREATE TABLE machines (
                machine_id VARCHAR(30) PRIMARY KEY,
                machine_name VARCHAR,
                imgpath TEXT,
                status VARCHAR,
                location_id VARCHAR  
            )
            """
        )
        
        for table in tables:
            cur.execute(table)
        cur.close()
        connection.commit()    
    except (Exception, pg.Error) as error:
        print('Error connecting to postgresDB', error)

'''
Populates database
'''
def pop_db():
    try:
        '''
        create new connection to connect to newly created db
        '''
        connection = pg.connect(dbname='challenge', user='postgres', password='root')
        cur = connection.cursor()

        insert_sensors = ''' INSERT INTO sensors(machine_id, sensor_id, sensor_name) VALUES(%s, %s, %s) '''
        insert_machines = ''' INSERT INTO machines(machine_id, machine_name, imgpath, status, location_id) VALUES(%s, %s, %s, %s, %s) '''
        
        pge.execute_batch(cur, insert_sensors, sensors_ls)
        pge.execute_batch(cur, insert_machines, machines_ls)
        connection.commit()

    except(Exception, pg.Error) as error:
        print(error)

'''
Set up initial connection to db server
'''
connection = pg.connect(user='postgres', password='root')
connection.autocommit=True

# init_db()
# init_tables()

sensors_df = pd.read_json('Sensors.json')
machines_df = pd.read_json('machines.json')


sensors_ls = sensors_df.values.tolist(); ''' convert to list for easy insertion'''
machines_ls = machines_df.values.tolist(); ''' convert to list for easy insertion'''

pop_db()