# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 11:27:55 2020

@author: Jost
"""


import pandas as pd
import numpy as np
import tabula
from tabula import read_pdf
import pandas_compat
import os
import geopandas as gpd


from pathlib import Path
import requests

os.chdir("C:/Users/Jost/Desktop/Master/Masterarbeit/python")


## import data 

df = pd.read_csv("data/2020.csv",header = None)
#df = df.head(10000)

# keep only daily max temp

df.head()
df = df.drop(df.columns[range(4,8)],axis = 1)
df.columns = ['ID','date','element','value']
df = df[df.element=="TMAX"]

# select italy

df = df[(df.ID.str[0]=="I") & (df.ID.str[1]=="T")]
df['date'] = pd.to_datetime(df["date"], format='%Y%m%d')

df = df.sort_values(['ID','date'])

# read station file 

lex = pd.read_fwf('data/ghcnd-stations.txt',header = None)

lex = lex.drop(range(5,8), axis = 1) 
lex.columns = ['ID','lat','long','unknown','region']
lex = lex[(lex.ID.str[0]=="I") & (lex.ID.str[1]=="T")]

# load shapefile to match lat and long to regions
data = gpd.read_file("path.mygeopackage.gpkg")
data.head() 