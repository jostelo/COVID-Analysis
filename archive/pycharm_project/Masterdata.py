#!/usr/bin/env python
# coding: utf-8

# In[1]:


#this Python 3 environment comes with many helpful analytics libraries installed


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import io
import requests

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


# In[2]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 300)


# In[3]:




owidurl = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

url = owidurl
s = requests.get(url).content
owid_ds = pd.read_csv(io.StringIO(s.decode('utf-8')))


# In[4]:


owid_ds.head()


# In[5]:


owid_ds.groupby(['location']).size()


# In[6]:


owid_ds.date=pd.to_datetime(owid_ds["date"])
owid_ds["mo"]=owid_ds["date"].dt.month
owid_ds["da"]=owid_ds["date"].dt.day
owid_ds=owid_ds[owid_ds.continent=="Europe"]
owid_ds=owid_ds.rename(columns={"location": "country"})
owid_ds.head()


# In[7]:


owid_ds.groupby(['country']).size()


# In[8]:


weather_master=pd.read_csv("data/weather_master.csv")
weather_master.head()
weather_master.day_from_jan_first


# In[9]:


weather_master.groupby(['country']).size()


# In[10]:


owid_ds.country.unique()


# In[11]:


df=pd.merge(owid_ds,weather_master,on=["country","mo","da"])


# In[12]:


df.groupby(['country']).size()


# In[13]:


df[["country","date","total_cases"]][df.new_cases.isnull()]


# In[14]:


df.to_csv("data/master")

