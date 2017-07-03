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
df1=pd.read_csv('StockPrices/SBI/SBI.csv')
df1 = df1[['Date','Close', 'Volume', 'MarketCap', 'PriceToBook', 'EV', 'MarketCapToSales', 'ROE', 'EPS', 'DIV', 'MA','Volatility']]
c=df1.columns.values
Cash=100000
path='StockPrices'
stocknames=os.listdir(path)
Cmax=3
n_stocks=4
Cash_max=Cash*Cmax/100.0
df1.set_index('Date',inplace=True)
# print(c)
#print(df1.head())
for date in df1.index:
    l=[]
    for col in df1.columns:
        l.append(df1.get_value(date,col))
    Ratios[date]=l
dates=list(Ratios.keys())
df_dict=dict()
for files in stocknames:
    df=pd.read_csv("StockPrices\\" + files + "\\" + files + ".csv")
    df.set_index('Date',inplace=True)
    df = df[['Close', 'Volume', 'MarketCap', 'PriceToBook', 'EV', 'MarketCapToSales', 'ROE', 'EPS', 'DIV', 'MA','Volatility']]
    df_dict[files]=df

with open('df_dict.pkl', 'wb') as f:
    pickle.dump(df_dict, f)
pset = gp.PrimitiveSet("MAIN", 11)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(operator.pow,2)
pset.renameArguments(ARG0=c[1],ARG1=c[2],ARG2=c[3],ARG3=c[4],ARG4=c[5],ARG5=c[6],ARG6=c[7],ARG7=c[8],ARG8=c[9],ARG9=c[10],ARG10=c[11])


creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMulti)


toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=2, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)
toolbox.register("prob",isBetter.probability)

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
with open('env_paretos//4pareto.pkl', 'rb') as f:
    pareto_guys = pickle.load(f)
print(len(pareto_guys))
max=0
for guy in pareto_guys:
    if(guy.fitness.values[0]>max):
        max=guy.fitness.values[0]
        test_guy=guy

print(test_guy)

del test_guy.fitness.values
fitnesses = evalStockRanking(test_guy)
# for guy, fit in zip(test_guy, fitnesses):
#     guy.fitness.values = fit
# print(test_guy[0].fitness.values)
