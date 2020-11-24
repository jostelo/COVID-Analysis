import numpy as np
import pandas as pd
import os

os.chdir("C:/Users/Jost/Desktop/Master/Masterarbeit/python")
data = pd.read_csv("data/RKI_COVID_individuals.csv")

data.head()