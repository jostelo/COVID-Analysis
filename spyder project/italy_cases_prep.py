# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 21:23:55 2020

@author: Jost
"""

## Pull Italy cases


import numpy as np # linear algebra
import pandas as pd
#import git
#from git import Repo
import os 
import sys

# options

pd.set_option('display.max_columns', 20)

#  Set working directory

import sys
import os

#path  = "C:/Users/Jost/Desktop/Master/Masterarbeit/python/data/italy_cases" 
#clone = "git clone https://github.com/pcm-dpc/COVID-19/tree/master/dati-regioni" 

#os.system("sshpass -p your_password ssh user_name@your_localhost")
#os.chdir(path) # Specifying the path where the cloned project needs to be copied
#print(os.system(clone))
#print(os.system(git))

# import data 

os.chdir("C:/Users/Jost/Desktop/Master/Masterarbeit/python")

files = os.listdir("C:/Users/Jost/Desktop/Master/Masterarbeit/python/data/italy_cases/COVID-19/dati-regioni")

df = pd.read_csv("C:/Users/Jost/Desktop/Master/Masterarbeit/python/data/italy_cases/COVID-19/dati-regioni/"+files[0])


for x in files[1:]:
    temp = pd.read_csv("C:/Users/Jost/Desktop/Master/Masterarbeit/python/data/italy_cases/COVID-19/dati-regioni/"+x)
    df = df.append(temp)

    
## Rename columns
df = df[['data', 'stato', 'codice_regione', 'denominazione_regione', 'lat', 'long', 'totale_positivi','nuovi_positivi', 'dimessi_guariti','deceduti','totale_casi', 'tamponi', 'casi_testati']]

df.columns = ['date', 'country', 'region_code', 'region', 'lat','long', 'total_current_positives',  'new_positives', 'recovered', 'dead', 'total_cases', 'tests','total_tests']

# population data

#url = 'https://www.tuttitalia.it/regioni/'
#lex = pd.read_html(url)[0]

#lex.to_csv("data/Italy_pop.csv")
lex = pd.read_csv("data/Italy_pop.csv", index_col = 0)

lex = lex[lex.columns[[1,2]]][:-1]

lex.columns = ["region","population"]

df = pd.merge(df,lex,how='inner',validate="m:1",left_on = 'region', right_on = 'region')  
