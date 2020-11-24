#!/usr/bin/env python
# coding: utf-8

# In[5]:


#this Python 3 environment comes with many helpful analytics libraries installed


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
import plotly.offline as py
py.init_notebook_mode(connected=True)

from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')


# options

pd.set_option('display.max_columns', 20)

#  Set working directory

os.chdir("C:/Users/Jost/Desktop/Master/Masterarbeit/python")

# Load  Germany data

df = pd.read_csv("data/RKI_COVID_individuals.csv")

#  Summarise data 

# Meldedatum = When was the case detected?
# Refdatum = When did the disease start? 


df.describe()
df.columns
df.head()

# convert to datetime

df.Meldedatum=pd.to_datetime(df["Meldedatum"])
df.Refdatum=pd.to_datetime(df["Refdatum"])

df2 = df[["Refdatum","Bundesland","ObjectId"]]
df2 = df2.groupby(by=["Refdatum","Bundesland"],as_index=False).count()
df2.head()
df2.dtypes
test = (df[['Meldedatum','Refdatum']])


#  Plot

fig, ax = plt.subplots(figsize=(10,8))
classes = list(df2.Bundesland.unique())
for c in classes:
    df3 = df2.loc[df2['Bundesland'] == c]
    df3.ObjectId.plot(x="Refdatum", ax=ax, label=c)
plt.legend()

# weekly mean

df["Woche"] = df.Refdatum.dt.week


df3 = df[["Bundesland","Woche","ObjectId"]]
df3 = df3.groupby(["Bundesland","Woche"],as_index=False).count()
df3.dtypes


fig, ax = plt.subplots(figsize=(10,8))
classes = list(df3.Bundesland.unique())
for c in classes:
    df4 = df3.loc[df3['Bundesland'] == c]
    df4.plot(x="Woche", y = "ObjectId" , ax=ax, label=c)
plt.legend()


# load wheather_master and merge

del [c,classes,df,df3,df4] 
df = df2
del df2
df.columns.values[1] = "Bundesland-Name" 
weather = pd.read_csv("data/weather_master.csv")
weather = weather.drop('Unnamed: 0',axis=1)

df=df.rename(columns = {'Bundesland-Name':'Bundeslandname'})
weather=weather.rename(columns = {'Bundesland-Name':'Bundeslandname'})
weather['Zeitstempel'] = pd.to_datetime(weather['Zeitstempel'], format='%Y%m%d')

df=df.rename(columns = {'Refdatum':'Zeitstempel'})


df = pd.merge(weather,df,how='outer',validate="m:1",left_on = ['Bundeslandname','Zeitstempel'], right_on = ['Bundeslandname','Zeitstempel'])  

df["ObjectId"] = df["ObjectId"].fillna(0)
df=df.rename(columns = {'ObjectId':'Cases'})
df=df.rename(columns = {'Wert':'Temp'})

df.to_csv("data/Germany_cases_weather.csv")

del weather 


# mean over weeks

df["Woche"] = df.Zeitstempel.dt.week

# lag time

df = df.sort_values(["Bundesland","Zeitstempel"])


df['Temp_shift_5'] = df.groupby(['Bundesland'])['Temp'].shift(4)
df['Temp_roll'] = df['Temp_shift_5'].rolling(5, win_type='gaussian').mean(std=3.9)



## state population

pop = pd.read_csv("data/germany_pop.csv", sep=';',header=None, encoding="latin1").T
pop = pop[[0,9]]
pop = pop.drop([0,1,2])
pop.columns = ["Bundeslandname", "population"]

df= pd.merge(df,pop,how='inner',validate="m:1",left_on = ['Bundeslandname'], right_on = ['Bundeslandname'])  

df["population"] = pd.to_numeric(df["population"])


## cases per capita 

df["cases_per_1000000"] = round(df["Cases"]*1000000/df["population"])


## Merge tests

tests =  pd.read_csv("data/tests_Germany.csv")

df['date'] = str(df['Zeitstempel'])
df['date'] = df['Zeitstempel'].dt.date
tests.date = pd.to_datetime(tests.date).dt.date
tests = tests.rename(columns={'Bundesland': 'Bundeslandname'})

df = pd.merge(tests,df,how='outer',validate="m:1",on = ['Bundeslandname','date'])  



df = df.drop(df.columns[[0,1]], axis=1)


df.to_csv("data/Germany_cases_weather.csv")



## drop observations by state which were before outbreak

#df["cum_cases"] = df.groupby("Bundesland").cumsum()["cases_per_1000000"]

#df = df.drop(df[df["cases_per_1000000"] < 1].index)


df["Cases"].corr(df["Temp_shift_5"])
