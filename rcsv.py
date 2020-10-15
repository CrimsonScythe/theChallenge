import pandas as pd
import csv
import pickle

FILENAME = 'Sensors\' values.csv'

'''
Fix the formatting on the csv
'''
df = pd.read_csv(FILENAME, sep=';')
df = df.replace(',', '', regex=True)
df.columns = df.columns.str.replace(',', '')
print(df)

with open ('sensor_values.pickle', 'wb') as file:
        pickle.dump(df, file)