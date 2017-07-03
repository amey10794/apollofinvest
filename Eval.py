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
from test import fitness_60
def eval_ind(ind,iter):
    Ratios=dict()
    df1=pd.read_excel('FMCG//Britania//Britania_final.xlsx')
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


    pset = gp.PrimitiveSet("MAIN", 11)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addPrimitive(operator.pow,2)
    pset.renameArguments(ARG0=c[1],ARG1=c[2],ARG2=c[3],ARG3=c[4],ARG4=c[5],ARG5=c[6],ARG6=c[7],ARG7=c[8],ARG8=c[9],ARG9=c[10],ARG10=c[11])

    creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMulti)
    # toolbox = base.Toolbox()
    # toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=2, max_=3)
    # toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    # toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    # toolbox.register("compile", gp.compile, pset=pset)
    func=gp.compile(ind,pset)
    avg_risk,avg_return=fitness_60(func,Cash=Cash,C_max=Cash_max,stocknames=stocknames,N_stocks=4,df_dict=df_dict,iter=iter)
    return avg_risk,avg_return,func

def eval_func(ind):
    Ratios=dict()
    df1=pd.read_csv('StockPrices/SBI/SBI.csv')
    df1 = df1[['Date','Close', 'Volume', 'MarketCap', 'PriceToBook', 'EV', 'MarketCapToSales', 'ROE', 'EPS', 'DIV', 'MA','Volatility']]
    c=df1.columns.values
    # Cash=100000
    # path='StockPrices'
    # stocknames=os.listdir(path)
    # Cmax=3
    # n_stocks=4
    # Cash_max=Cash*Cmax/100.0
    # df1.set_index('Date',inplace=True)
    # # print(c)
    # #print(df1.head())
    # for date in df1.index:
    #     l=[]
    #     for col in df1.columns:
    #         l.append(df1.get_value(date,col))
    #     Ratios[date]=l
    # dates=list(Ratios.keys())
    # df_dict=dict()
    # for files in stocknames:
    #     df=pd.read_csv("StockPrices\\" + files + "\\" + files + ".csv")
    #     df.set_index('Date',inplace=True)
    #     df = df[['Close', 'Volume', 'MarketCap', 'PriceToBook', 'EV', 'MarketCapToSales', 'ROE', 'EPS', 'DIV', 'MA','Volatility']]
    #     df_dict[files]=df


    pset = gp.PrimitiveSet("MAIN", 11)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addPrimitive(operator.pow,2)
    pset.renameArguments(ARG0=c[1],ARG1=c[2],ARG2=c[3],ARG3=c[4],ARG4=c[5],ARG5=c[6],ARG6=c[7],ARG7=c[8],ARG8=c[9],ARG9=c[10],ARG10=c[11])

    creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMulti)
    # toolbox = base.Toolbox()
    # toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=2, max_=3)
    # toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    # toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    # toolbox.register("compile", gp.compile, pset=pset)
    func=gp.compile(ind,pset)
    return func
