

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


# In[3]:


pd.set_option('display.max_columns', None)
def movecol(df, cols_to_move=[], ref_col='', place='After'):
    
    cols = df.columns.tolist()    
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    if place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]
    
    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]
    
    return(df[seg1 + seg2 + seg3])


# In[4]:


df=pd.read_csv("data/master")

# convert from fahrenheit to celsius; 
for x in ["temp","min","max"]:
    df[x]=(df[x]-32)*(5/9)

# rolling mean of temperature and cases  
for x in ["temp","min","max","new_cases_per_million"]:
    new_col=df.groupby('country',as_index=False)[x].rolling(3).mean()
    new_col=new_col.reset_index(level=0, drop=True)
    df[str(x+"_roll")]=new_col
df=df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
df["new_cases_per_million"]=round(df.new_cases_per_million)
df = movecol(df, 
             cols_to_move=["day_from_jan_first","mo","da"], 
             ref_col='date',
             place='After')
df.head()


# In[5]:


d=df.groupby(['country']).size().to_dict()


# l=[]
# for key in l: 
#     if d[key]==181:
#         print(key)
#         d.append(key)
# l
#         

# In[ ]:





# In[5]:


df[df.country.isin(["Germany","Italy"])]


# In[6]:


df_ger=df[(df.country=="Germany") & (df.day_from_jan_first>50) ]
df_ita=df[(df.country=="Italy")& (df.day_from_jan_first>50)]
plt.bar(x=df_ger.day_from_jan_first, height=df_ger.new_cases_per_million,width=0.3,label="Germany")
plt.bar(x=df_ita.day_from_jan_first+0.3, height=df_ita.new_cases_per_million,width=0.3,label="Italy")
plt.legend(loc="upper left")#plt.show()
plt.ylabel('New cases per million inhabitants', fontsize=10)
plt.xlabel('Days since January the 1st', fontsize=10)
plt.savefig('plots/new_cases_ger_ita.png',dpi=300)
plt.savefig('C:/Users/Jost/Desktop/Master/Masterarbeit/TeX/plots/new_cases_ger_ita.png',dpi=300)


# In[7]:


df_ger


# In[8]:


df[df.population>5000000]


# In[9]:


#Adjust for country-specific start points of covid outbreak. A country should at least have 5 infected per million
df=df[(df.total_cases_per_million>5) & (df.population>5000000)]
df.country.unique()


# In[10]:


# First glance at dependency of temp and cases

df.plot.scatter(x='temp', y='total_cases')


# In[11]:


df.plot.scatter(x='temp', y='new_cases_per_million')


# In[12]:


# lag the variable temp

df['temp_10_shifted'] = df.groupby(['country'])['temp'].shift(10)
df.plot.scatter(x='temp_10_shifted', y='new_cases_per_million')


# In[13]:


df[(df['temp']>25) & (df['new_cases_per_million']>200)]


# In[14]:


t_y=df['new_cases_per_million'][(df['new_cases_per_million']>=0) & (df['new_cases_per_million']<200) ]
t_x=df['temp_10_shifted'][(df['new_cases_per_million']>=0) & (df['new_cases_per_million']<200) ]
t_x.head()


# In[15]:


plt.scatter(t_x,t_y)

