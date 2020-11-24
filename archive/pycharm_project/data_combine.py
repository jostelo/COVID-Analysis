#!/usr/bin/env python
# coding: utf-8

# In this notebook I add weather informations, such as temperature and precipitations, to the training set of the [COVID-19 forecasting competition](https://www.kaggle.com/c/covid19-global-forecasting-week-1/discussion), in order to determine whether there is any correlation with the growth of confirmed cases. Weather data is imported from the [NOAA GSOD dataset](https://www.kaggle.com/noaa/gsod), continuously updated to include recent measurments.
# 
# [Data for this and previous weeks is available in dataset form here.](https://www.kaggle.com/davidbnn92/weather-data-for-covid19-data-analysis)
# 
# Edit: now missing values are denoted with usual `NaN`s, and not with `9999`s.
# 
# Edit 2: information concerning humidity was added, following [brennanmurphy](https://www.kaggle.com/brennanmurphy)'s advice. More specifically, dewpoint temperature was added from the NOAA GSOD dataset, then absolute and relative humidity were computed.

# In[1]:


import numpy as np
import pandas as pd

import os
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.spatial.distance import cdist

for dirname, _, filenames in os.walk('/kaggle/input'):
    print(dirname)

from google.cloud import bigquery



# Here is the weather data:
# * `temp`: Mean temperature for the day in degrees Fahrenheit to tenths.
# * `max`: Maximum temperature reported during the day in Fahrenheit to tenths--time of max temp report varies by country and region, so this will sometimes not be the max for the calendar day.
# * `min`: Minimum temperature reported during the day in Fahrenheit to tenths--time of min temp report varies by country and region, so this will sometimes not be the min for the calendar day.
# * `stp`: Mean station pressure for the day in millibars to tenths.
# * `slp`: Mean sea level pressure for the day in millibars to tenths.
# * `dewp`: Mean dew point for the day in degrees Fahrenheit to tenths. 
# * `wdsp`: Mean wind speed for the day in knots to tenths.
# * `prcp`: Total precipitation (rain and/or melted snow) reported during the day in inches and hundredths; will usually not end with the midnight observation--i.e., may include latter part of previous day. .00 indicates no measurable precipitation (includes a trace).
# * `fog`: Indicators (1 = yes, 0 = no/not reported) for the occurrence during the day

# In[2]:


def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


# In[3]:


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\Jost\Desktop\covid-304dab3f9983.json"


# In[18]:


implicit()


# In[4]:


client = bigquery.Client()
dataset_ref = client.dataset("noaa_gsod", project="bigquery-public-data")
dataset = client.get_dataset(dataset_ref)

tables = list(client.list_tables(dataset))

table_ref = dataset_ref.table("stations")
table = client.get_table(table_ref)
stations_df = client.list_rows(table).to_dataframe()

table_ref = dataset_ref.table("gsod2020")
table = client.get_table(table_ref)
twenty_twenty_df = client.list_rows(table).to_dataframe()

stations_df['STN'] = stations_df['usaf'] + '-' + stations_df['wban']
twenty_twenty_df['STN'] = twenty_twenty_df['stn'] + '-' + twenty_twenty_df['wban']

cols_1 = ['STN', 'mo', 'da', 'temp', 'min', 'max', 'stp', 'slp', 'dewp', 'wdsp', 'prcp', 'fog']
cols_2 = ['STN', 'country', 'state', 'call', 'lat', 'lon', 'elev']
weather_df = twenty_twenty_df[cols_1].join(stations_df[cols_2].set_index('STN'), on='STN')

weather_df['temp'] = weather_df['temp'].apply(lambda x: np.nan if x==9999.9 else x)
weather_df['max'] = weather_df['max'].apply(lambda x: np.nan if x==9999.9 else x)
weather_df['min'] = weather_df['min'].apply(lambda x: np.nan if x==9999.9 else x)
weather_df['stp'] = weather_df['stp'].apply(lambda x: np.nan if x==9999.9 else x)
weather_df['slp'] = weather_df['slp'].apply(lambda x: np.nan if x==9999.9 else x)
weather_df['dewp'] = weather_df['dewp'].apply(lambda x: np.nan if x==9999.9 else x)
weather_df['wdsp'] = weather_df['wdsp'].apply(lambda x: np.nan if x==999.9 else x)
weather_df['prcp'] = weather_df['prcp'].apply(lambda x: np.nan if x==99.9 else x)

display(weather_df.tail(10))
weather_df.info(verbose=True)


# Now let's compute absolute and relative humidity from temperature and dew point:

# In[1]:


# convert everything into celsius
temp = (weather_df['temp'] - 32) / 1.8
dewp = (weather_df['dewp'] - 32) / 1.8
    
# compute relative humidity as ratio between actual vapour pressure (computed from dewpoint temperature)
# and saturation vapour pressure (computed from temperature) (the constant 6.1121 cancels out)
weather_df['rh'] = (np.exp((18.678*dewp)/(257.14+dewp))/np.exp((18.678*temp)/(257.14+temp)))

# calculate actual vapour pressure (in pascals)
# then use it to compute absolute humidity from the gas law of vapour 
# (ah = mass / volume = pressure / (constant * temperature))
weather_df['ah'] = ((np.exp((18.678*dewp)/(257.14+dewp))) * 6.1121 * 100) / (461.5 * temp)


# In[2]:


weather_df.head()


# In[139]:


weather_df.to_csv("data/weather.csv")


# In[2]:


weather_df=pd.read_csv("data/weather.csv")


# In[3]:


weather_df.groupby(['STN']).size()


# In[4]:


weather_df=weather_df.groupby('STN').filter(lambda x : len(x)>180)


# In[5]:


train=pd.read_csv("data/train.csv")
train=train[["Country/Region","Lat","Long"]]
train=train.drop_duplicates()
train=train.rename(columns={"Country/Region":"country"})

train.head()


# In[6]:


train.groupby('country').filter(lambda x : len(x)>1).country.unique()


# In[7]:


train[train.country=="France"]


# In[8]:


# Drop if country has mmultiple parts over the world
train=train[(train.country!="United Kingdom") & (train.Lat!=49.3723)]
train=train[(train.country!="Netherlands") & (train.Lat!= 52.1326)]
train=train[(train.country!="Denmark") & (train.Lat!= 56.2639)]
train=train[(train.country!="France") & (train.Lat!= 46.2276)]


# In[9]:



weather_df.head()


# In[10]:


weather_stations=weather_df[["STN","lat","lon"]]


# In[11]:


weather_stations=weather_stations.drop_duplicates()
weather_stations.head()


# In[12]:


output = pd.DataFrame()

for _,row in train.iterrows():
    C={"country":row["country"],"Distance":10000000}

    for _,row2 in weather_stations.iterrows():
        dist=(row["Lat"]-row2["lat"])**2+(row["Long"]-row2["lon"])**2
        if dist< C["Distance"]: 
            C={"country":row["country"],"STN":row2["STN"],"Distance":dist,"lat_st":row2["lat"],"long_st":row2["lon"]}

    output=output.append(C,ignore_index=True)


# In[15]:


output.to_csv("matched_stations")
output.head()


# In[14]:


weather_df['day_from_jan_first'] = (weather_df['da'].apply(int)
                                   + 31*(weather_df['mo']=='02') 
                                   + 60*(weather_df['mo']=='03')
                                   + 91*(weather_df['mo']=='04')
                                   + 121*(weather_df['mo']=='05')  
                                   + 152*(weather_df['mo']=='06')  
                                   + 182*(weather_df['mo']=='07')  
                                   + 213*(weather_df['mo']=='08')  
                                   + 244*(weather_df['mo']=='09')  
                                   + 274*(weather_df['mo']=='10')  
                                   + 305*(weather_df['mo']=='11')  
                                   + 335*(weather_df['mo']=='12'))


# In[37]:


weather_df['day_from_jan_first'] = (weather_df['da']
                                       + 31*(weather_df['mo']==2) 
                                       + 60*(weather_df['mo']==3)
                                       + 91*(weather_df['mo']==4)
                                       + 121*(weather_df['mo']==5)  
                                       + 152*(weather_df['mo']==6)  
                                       + 182*(weather_df['mo']==7)  
                                       + 213*(weather_df['mo']==8)  
                                       + 244*(weather_df['mo']==9)  
                                       + 274*(weather_df['mo']==10)  
                                       + 305*(weather_df['mo']==11)  
                                       + 335*(weather_df['mo']==12))


# In[38]:


weather_df[weather_df['STN'].isin(output["STN"])]
weather_df.head()


# In[35]:


#weather_df=weather_df.drop(["country","state"],1)
335*(weather_df['mo']==1)


# In[39]:


weather_master=pd.merge(weather_df, output)
weather_master.head(200)


# In[40]:


weather_master.groupby(['country']).size()


# In[41]:


weather_master.groupby('country').filter(lambda x : len(x)>181)["country"].unique()


# In[42]:


weather_master.to_csv("data/weather_master.csv")

