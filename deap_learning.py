from deap import base, creator, gp
import matplotlib.pyplot as plt
import multiprocessing
import pickle
import numpy

### Graphviz Section ###

from deap import algorithms
import operator
from scipy.stats import spearmanr
import test
import numpy as np
import pandas as pd
from deap import tools
import os
import isBetter
import monthly_test
Ratios=dict()
df1=pd.read_excel('FMCG//Britania//Britania_final.xlsx',sheetname=0)
df1 = df1[['Date', 'Price', 'Volume', 'MarketCap', 'PE', 'PB','ProfitMargin','ROA', 'DebtEquity','CurrentRatio', 'InventoryTurnover','DividendPayout','CrudePrice','GoldPrice','Inflation','Forex','GDP','MA','Volatility','RepoRate','FII']]
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
    df =df[['Price', 'Volume', 'MarketCap', 'PE', 'PB','ProfitMargin','ROA', 'DebtEquity','CurrentRatio', 'InventoryTurnover','DividendPayout','CrudePrice','GoldPrice','Inflation','Forex','GDP','MA','Volatility','RepoRate','FII']]
    df_dict[files]=df


with open('df_dict.pkl', 'wb') as f:
    pickle.dump(df_dict, f)
pset = gp.PrimitiveSet("MAIN", 20)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(operator.pow_2,1)
pset.addPrimitive(operator.pow_3,1)
pset.addPrimitive(operator.my_div,2)
pset.renameArguments(ARG0='Price',ARG1='Volume',ARG2='MarketCap',ARG3='PE',ARG4='PB', ARG5='ProfitMargin',ARG6='ROA',ARG7='DebtEquity',ARG8='CurrentRatio',ARG9='InventoryTurnover',ARG10='DividendPayout',ARG11='CrudePrice',ARG12='GoldPrice',ARG13='Inflation',ARG14='Forex',ARG15='GDP',ARG16='MA',ARG17='Volatility',ARG18='RepoRate',ARG19='FII')


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
    with open('month.pkl', 'rb') as f:
        month = pickle.load(f)

    avg_ret,avg_risk=test.fitness_trailing(func=func,Cash=Cash,C_max=Cash_max,N_stocks=4,df_dict=df_dict,stocknames=stocknames,iter=iter,month=month)
    plt.scatter(avg_ret,avg_risk)
    # print("Return"+str(avg_ret))
    # print("Risk"+str(avg_risk))
    return avg_ret,avg_risk

def evalStockTesting(individual):
    func = toolbox.compile(expr=individual)
    with open('iter.pkl', 'rb') as f:
        iter = pickle.load(f)
    with open('month.pkl', 'rb') as f:
        month=pickle.load(f)
    avg_ret=monthly_test.fitness_trailing_test(func=func,Cash=Cash,C_max=Cash_max,N_stocks=4,df_dict=df_dict,stocknames=stocknames,iter=iter,month=month)

    # print("Return"+str(avg_ret))
    # print("Risk"+str(avg_risk))
    return avg_ret
MAX_LIMIT=17
toolbox.register("evaluate", evalStockRanking)
toolbox.register("select", tools.selSPEA2)
toolbox.register("mate", gp.cxOnePoint)
toolbox.decorate("mate",gp.staticLimit(operator.attrgetter('height'),MAX_LIMIT))
toolbox.register("expr_mut", gp.genGrow, min_=2, max_=3)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.decorate("mutate",gp.staticLimit(operator.attrgetter('height'),MAX_LIMIT))


def update_memory(mem_pop):
    with open('memory.pkl', 'wb') as f:
        pickle.dump(mem_pop, f)

def main(pool):
    toolbox.register("map", pool.map)
    if os.path.isfile('checkpoint_name.pkl'):
        with open('checkpoint_name.pkl', "rb") as cp_file:
            cp = pickle.load(cp_file)
        pop = cp["population"]
        start_gen = cp["generation"]
        hof = cp["halloffame"]
        logbook = cp["logbook"]

    else:
        # Start a new evolution
        pop = toolbox.population(n=300)
        start_gen = 0
        hof = tools.HallOfFame(maxsize=5)
        logbook = tools.Logbook()
    with open('iter.pkl', 'rb') as f:
        iter_pk = pickle.load(f)
    #randomize the search population and pickle with fitness
    rand_pop=toolbox.population(n=300)
    fitnesses_rand = toolbox.map(toolbox.evaluate, rand_pop)
    for ind, fit in zip(rand_pop, fitnesses_rand):
        ind.fitness.values = fit
    with open('search_pop.pkl', 'wb') as f:
        pickle.dump(rand_pop, f)
    #assign fitness values to last envs pop for new env
    for ind in pop:
        del ind.fitness.values
    fitnesses_pop = toolbox.map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses_pop):
        ind.fitness.values = fit
    with open('env_final_pop/' + str(iter_pk) + 'pop.pkl', 'wb') as f:
        pickle.dump(pop, f)
    #unpickle the memory
    if (os.path.isfile('memory.pkl')):
        with open('memory.pkl', 'rb') as f:
            memory=pickle.load(f)
        for mem in memory:
            del mem.fitness.values
        fitnesses_mem = toolbox.map(toolbox.evaluate, memory)
        for mem, fit in zip(memory, fitnesses_mem):
            mem.fitness.values = fit

        with open('env_memory/' + str(iter_pk) + 'memory.pkl', 'wb') as f:
            pickle.dump(mem, f)
        # print(len(memory))
        # print(len(pop))
        pop=pop+memory

        # print("ADDED POP"+str(len(pop)))
    else:
        pop=pop
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    # print("LEN",len(pop))
    # for ind in pop:
    #     print(ind.fitness.values)
    pop,log=algorithms.eaMuPlusLambda(0,pop, toolbox,300,300, 0.8, 0.1, 20, stats, halloffame=hof)
    pool.close()
    return pop, stats, hof


if __name__ == "__main__":

    if (os.path.isfile('iter.pkl')):
        with open('iter.pkl', 'rb') as f:
            iter_pk = pickle.load(f)
    else:
        iter_pk = 0

    for iter in range(iter_pk, 9):
        print(iter)
        month_pk=0
        for month in range(month_pk, 12):
            print(month)
            with open('iter.pkl', 'wb') as f:
                pickle.dump(iter, f)
            with open('month.pkl', 'wb') as f:
                pickle.dump(month, f)
            pool = multiprocessing.Pool(processes=4)
            population, stats, hof = main(pool)
            with open("HOF//"+iter+"_"+month+"hof.pkl","wb") as f:
                pickle.dump(hof,f)
            with open("POP//"+iter+"_"+month+"pop.pkl","wb") as f:
                pickle.dump(population,f)