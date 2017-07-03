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
    avg_ret,avg_risk=test.fitness_trailing(func=func,Cash=Cash,C_max=Cash_max,N_stocks=4,df_dict=df_dict,stocknames=stocknames,iter=7,month=0)
    plt.scatter(avg_ret,avg_risk)
    # print("Return"+str(avg_ret))
    # print("Risk"+str(avg_risk))
    return avg_ret,avg_risk,

toolbox.register("evaluate", evalStockRanking)
toolbox.register("select", tools.selSPEA2)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=3, max_=5)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
#
with open('checkpoint_name.pkl', "rb") as cp_file:
        cp = pickle.load(cp_file)
pop = cp["population"]
start_gen = cp["generation"]
hof = cp["halloffame"]
print(start_gen)
print(len(pop))
for ind in pop:
    print(ind.fitness.values)
# cp["population"]=pop[:7]
# with open('checkpoint_name.pkl', "wb") as cp_file:
#     pickle.dump(cp,cp_file)
# with open('memory.pkl', "rb") as cp_file:
#         pop = pickle.load(cp_file)
# for ind in pop:
#     print(ind)
# pop=pop[:5]
# with open('memory.pkl', "wb") as mem:
#     pickle.dump(pop,mem)
# for ind in pop:
#     print(ind.fitness.values)
# with open('env_paretos//7_0pareto.pkl', "rb") as cp_file:
#         pop = pickle.load(cp_file)
# print(len(pop))
# ind=pop[100]
# ret,risk=evalStockRanking(ind)
# print(ret,risk)
# # #
# max_fit=0
# for ind in pop:
#     # print(ind.fitness.values)
#     if ind.fitness.values[0]>max_fit:
#         max_fit=ind.fitness.values[0]
#         best_ind=ind
#
# print(best_ind.fitness.values,"fitness")
# # if (os.path.isfile('iter.pkl')):
# #     with open('iter.pkl', 'rb') as f:
# #         iter_pk = pickle.load(f)
# #         print(iter_pk)
#
# ret,risk=evalStockRanking(best_ind)
# print(ret)
# print(risk)
# #
# print(len(pop))
# for ind in pop:
#     print(ind.height)

# with open("bloat_pop.pkl","wb") as f:
#     pickle.dump(bloat_pop,f)
#
