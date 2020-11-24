#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


weather_df=pd.read_csv("data/weather_master.csv")


# In[5]:


weather_df.head()


# In[12]:


temp=weather_df[["country","long_st","lon"]]


# In[13]:


temp.drop_duplicates()

