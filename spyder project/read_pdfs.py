# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 11:12:24 2020

@author: Jost
"""




import pandas as pd
import numpy as np
import tabula
from tabula import read_pdf
import pandas_compat
import os


from pathlib import Path
import requests

os.chdir("C:/Users/Jost/Desktop/Master/Masterarbeit/python")

## add here new dates with Wochenberichten

datelist = ['0424','0429','0506','0513','0519','0526','0602','0610','0617','0624','0630','0707','0714','0721','0728','0804','0818','0825']

## only execute, if added a new wochenbericht 

#for x in datelist:
#    filename = Path('data/rki_wochenberichte/'+x+'.pdf')
#    url = 'http://ars.rki.de/Docs/SARS_CoV2/Wochenberichte/2020'+x+'_wochenbericht.pdf'
#    response = requests.get(url)
#    filename.write_bytes(response.content)    
#####    
df_list = []

col2str = {'dtype': str}
kwargs = {'output_format': 'dataframe',
          'pandas_options': col2str,
          'stream': True}
    
for x in os.listdir('data/rki_wochenberichte/'):
    df_list.append(tabula.read_pdf('data/rki_wochenberichte/'+x, pages = ['2'], multiple_tables = False,**kwargs)[0])
    print(x)

# clean some misread dataframes

df_list[0] = df_list[0].drop(df_list[0].index[[7,9]])
df_list[0].loc[df_list[0].Bundesland.isna(),'Bundesland' ] = 'Mecklenburg-Vorpommern' 
df_list[2] = pd.DataFrame(np.vstack([df_list[2].columns, df_list[2]]))
df_list[2].columns = df_list[1].columns
df_list[2].columns = df_list[0].columns

for x in range(0,18):
    print(x)
    df_list[x]['date'] = datelist[x] 
    
for x in range(0,18):
    df_list[x].columns = df_list[17].columns
    
df = df_list[0]

for x in range(1,18):
    df = df.append(df_list[x])
    
df["year"] = 2020
df['month'] = df['date'].str[:2]
df['day'] = df['date'].str[2:4]
df = df.drop('date',axis=1)

df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

df = df.drop(['year','month','day'],axis = 1)
df.columns= ['Bundesland', 'tests', 'pos_tests', 'pos_tests_perc', 'date']



#df.loc[df.tests.str.len() > 7, 'tests'] = df.loc[df.tests.str.len() > 7,'tests'].str.replace('.','')
df['tests'] = df.tests.str.replace('.', '')
df['pos_tests'] = df.pos_tests.str.replace('.', '')

df['tests'] = pd.to_numeric(df['tests'])#, errors='coerce')
df['pos_tests'] = pd.to_numeric(df['pos_tests'])#, errors='coerce')
df['tests_shift_1'] = df.groupby(['Bundesland'])['tests'].shift(1)
df['pos_tests_shift_1'] = df.groupby(['Bundesland'])['pos_tests'].shift(1)
df['new_tests'] = df['tests'] - df['tests_shift_1']

# drop Gesamt

df.loc[df.new_tests.isna(), 'new_tests'] = df.loc[df.new_tests.isna(),'tests']

df = df.drop(df[df.Bundesland == "Gesamt"].index)
df = df.drop(["tests","tests_shift_1","pos_tests_shift_1"],axis=1)
df['pos_tests_perc'] = df.pos_tests/df.new_tests


# save as csv 

df.to_csv('data/tests_Germany.csv')

    
