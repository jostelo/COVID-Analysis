#!/usr/bin/env python
# coding: utf-8

# In[5]:


#this Python 3 environment comes with many helpful analytics libraries installed


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import io
import requests
import os
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
from plotly import tools
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')


# options

pd.set_option('display.max_columns', 20)

#  Set working directory

os.chdir("C:/Users/Jost/Desktop/Master/Masterarbeit/python")

# Load  Germany data

df = pd.read_csv("data/Germany_weather_dwd/cdc_max_germany/data/data_TXK_MN004.csv")
df.head()

geo_df = pd.read_csv("data/Germany_weather_dwd/cdc_max_germany/data/sdo_TXK_MN004.csv")
geo_df.head()
geo_df = geo_df.drop("Metadata_Link",axis=1)


url = 'https://www.dwd.de/DE/leistungen/klimadatendeutschland/statliste/statlex_html.html?view=nasPublication&nn=16102'
lex = pd.read_html(url)[0]
lex.columns = lex.columns.droplevel()
lex.columns[1]
lex = lex.drop(["Kennung","Stations-kennung","Stations-höhe","Flussgebiet","Beginn","Ende"],axis=1)
lex = lex.drop_duplicates()
lex.to_csv("data/Germany_weather_dwd/lex.csv")

# Merge all three dataframes

df_temp = pd.merge(df,geo_df,validate="m:1",left_on = "SDO_ID", right_on = "SDO_ID")
df = pd.merge(df_temp,lex,validate="m:1",left_on = "SDO_ID", right_on = "Stations_ID")

# Test, whether all stations are correctly merged

test = np.array([df["Geogr_Breite"]-df["Breite"],df["Geogr_Laenge"]-df["Länge"]])
np.any(test>0.01)

# drop unused cols

df.columns
df = df.drop(['Produkt_Code','Qualitaet_Byte','SDO_Name','Qualitaet_Niveau','Geogr_Laenge', 'Geogr_Breite','Hoehe_ueber_NN'],axis=1)

# convert Bundesländer

url = 'https://www.dwd.de/DE/leistungen/klimadatendeutschland/stationsliste.html'
lex = pd.read_html(url)[1]

lex2 = lex.drop(lex.columns[[0,1]],axis=1)
lex2.columns = ["Bundesland", "Bundesland-Name"]
lex = lex.drop(lex.columns[[2,3]],axis=1)

lex = lex.append(lex2)


df = pd.merge(df,lex,validate="m:1",left_on = "Bundesland", right_on = "Bundesland")

df = df[["Zeitstempel", "Wert" , "Bundesland", "Bundesland-Name"]]


# mean temperature over date and Bundesland 

df = df.groupby(["Zeitstempel", "Bundesland", "Bundesland-Name"],as_index=False).mean()


# reformat date

#df['Zeitstempel'] = pd.to_datetime(df['Zeitstempel'], format='%Y%m%d')

# save data 

df.to_csv("data/weather_master.csv")

