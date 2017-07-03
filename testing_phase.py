import pickle
import matplotlib.pyplot as plt
from datetime import datetime
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


pset = gp.PrimitiveSet("MAIN", 11)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(operator.pow, 2)


creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=2, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)  # Start a new evolution

toolbox.register("select", tools.selSPEA2)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=2, max_=5)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
fig,ax=plt.subplots(nrows=1,ncols=1)
pareto_env=[]
for i in range(5):
    with open('env_paretos//'+str(i)+'pareto.pkl', 'rb') as f:
            pareto_guys = pickle.load(f)
    pareto_env.append(pareto_guys)
x=[]
y=[]
t=['x','D','^','o','*']
c=[(0.07,0.66,0.86),(1, 0, 0.501),(0.55,0.89,0.04),'orange','purple']
i=-1
l=[]
for pareto_guys in pareto_env:
    i=i+1
    for guy in pareto_guys:
            x.append(guy.fitness.values[1])
            y.append(guy.fitness.values[0])
    lo= plt.scatter(x,y,marker=t[i],color=c[i],s=25.0)
    l.append(lo)
    x=[]
    y=[]

plt.legend(tuple(l),('2007 environment', '2008 environment', '2009 environment', '2010 environment', '2011 environment'),
           scatterpoints=1,
           loc='upper right',
           ncol=3,
           fontsize=8)
plt.xlabel('Risk')
plt.ylabel('Return')

number=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
fig.savefig('pareto//'+str(number)+'.png')


