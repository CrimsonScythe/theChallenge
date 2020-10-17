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
for col in df:
        if (col=='Date time'):
                print('yes')
                continue
        df[col] = pd.to_numeric(df[col])
print(df)

with open ('sensor_values.pickle', 'wb') as file:
        pickle.dump(df, file)