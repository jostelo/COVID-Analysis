# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 11:53:10 2020

@author: Jost
"""



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

df = pd.read_csv("data/Germany_cases_weather.csv")


fig, ax = plt.subplots(figsize=(10,8))
classes = list(df.Bundesland.unique())
for c in classes:
    df3 = df.loc[df['Bundesland'] == c]
    df3.Cases.plot(x="date", ax=ax, label=c)
plt.legend()


fig, ax = plt.subplots(figsize=(10,8))
df.loc[df['Bundesland'] == "BY"].Cases.plot(x="date", ax=ax, label="Bayern")
df3.Cases.plot(x="date", ax=ax, label="Bayern")
plt.legend()
