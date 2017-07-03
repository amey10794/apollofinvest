from deap import base, creator, gp
import matplotlib.pyplot as plt
import multiprocessing
import pickle
import networkx as nx
### Graphviz Section ###
#import pygraphviz as pgv
from deap import algorithms
import operator
from scipy.stats import spearmanr
import test
import numpy as np
import pandas as pd
from deap import tools
import os
import isBetter
import collections
import numpy
Ratios=dict()
df1=pd.read_excel('FMCG//Britania//Britania_final.xlsx',sheetname=0)
df1 = df1[['Date', 'Price', 'Volume', 'MarketCap', 'PE', 'PB', 'ROA', 'CurrentRatio', 'InventoryTurnover','DividendPayout','CrudePrice','GoldPrice','Inflation','Forex','GDP']]
c=df1.columns.values
# print(c)
Cash=100000
path='FMCG'
stocknames=os.listdir(path)
Cmax=3
n_stocks=4
Cash_max=Cash*Cmax/100.0
df1.set_index('Date',inplace=True)

#print(df1.head())
for date in df1.index:
    l=[]
    for col in df1.columns:
        l.append(df1.get_value(date,col))
    Ratios[date]=l
dates=list(Ratios.keys())
df_dict=dict()
for files in stocknames:
    df=pd.read_excel("FMCG//" + files + "//" + files + "_final.xlsx",sheetname=0)
    df.set_index('Date',inplace=True)
    df = df[['Price', 'Volume', 'MarketCap', 'PE', 'PB', 'ROA', 'CurrentRatio', 'InventoryTurnover','DividendPayout','CrudePrice','GoldPrice','Inflation','Forex','GDP']]
    df_dict[files]=df


with open('df_dict.pkl', 'wb') as f:
    pickle.dump(df_dict, f)
pset = gp.PrimitiveSet("MAIN", 14)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)

pset.renameArguments(ARG0='Price',ARG1='Volume',ARG2='MarketCap',ARG3='PE',ARG4='PB',ARG5='ROA',ARG6='CurrentRatio',ARG7='InventoryTurnover',ARG8='DividendPayout',ARG9='CrudePrice',ARG10='GoldPrice',ARG11='Inflation',ARG12='Forex',ARG13='GDP')


creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMulti)


toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=2, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)
toolbox.register("prob",isBetter.probability)
toolbox.register("trailing_prob",isBetter.trailing_probability)
def evalStockRanking(individual):
    func = toolbox.compile(expr=individual)
    with open('iter.pkl', 'rb') as f:
        iter = pickle.load(f)
    avg_ret,avg_risk=test.fitness_60(func=func,Cash=Cash,C_max=Cash_max,N_stocks=4,df_dict=df_dict,stocknames=stocknames,iter=5)
    plt.scatter(avg_ret,avg_risk)
    # print("Return"+str(avg_ret))
    # print("Risk"+str(avg_risk))
    return avg_ret,avg_risk,

toolbox.register("evaluate", evalStockRanking)
toolbox.register("select", tools.selSPEA2)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=3, max_=5)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

# with open('checkpoint_name.pkl', "rb") as cp_file:
#         cp = pickle.load(cp_file)
# pop = cp["population"]
# start_gen = cp["generation"]
# hof = cp["halloffame"]
with open('env_paretos//4pareto.pkl', "rb") as cp_file:
        pop = pickle.load(cp_file)
print(len(pop))
#


for ind in pop:
    # print("======================================================")
    # print(ind.fitness.values)
    min=10000000
    if(ind.fitness.values[1]<min):
        min_ind=ind
        min=ind.fitness.values[1]
ind_list=[]
dist_list=[]
distance_dict=dict()
for ind in pop:
    dist=numpy.linalg.norm(numpy.array(ind.fitness.values) - numpy.array(min_ind.fitness.values))
    if dist not in dist_list:
        dist_list.append(dist)
        ind_list.append(ind)
        distance_dict[dist]=ind
# print(len(ind_list))
# print(sorted(dist_list))
od = collections.OrderedDict(sorted(distance_dict.items()))
median=int(len(od)/2)
count=0
final_list=[]
final_dist=[]
for k,v in od.items():
    if count==0:
        final_list.append(v)
        final_dist.append(k)
    elif count==median:
        final_list.append(v)
        final_dist.append(k)
    elif count==len(od)-1:
        final_list.append(v)
        final_dist.append(k)
    count+=1
for ind in final_list:
    ret,risk=evalStockRanking(ind)
    break
# for ind in final_list:
#     print(ind)
#     print(ind.height)
# print(final_dist)

# if (os.path.isfile('iter.pkl')):
#     with open('iter.pkl', 'rb') as f:
#         iter_pk = pickle.load(f)
#         print(iter_pk)
#

# #
# print(len(pop))
# for ind in pop:
#     print(ind.height)

# with open("bloat_pop.pkl","wb") as f:
#     pickle.dump(bloat_pop,f)
#
