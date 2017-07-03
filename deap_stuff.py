import random
import operator
import csv
import itertools
import pandas as pd
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
ctr=0
Ratios=dict()
df1=pd.read_csv('SBI.csv')
df1.set_index('Date',inplace=True)
#print(df1.head())
for date in df1.index:
    l=[]
    for col in df1.columns:
        l.append(df1.get_value(date,col))
    Ratios[date]=l
print(Ratios)
