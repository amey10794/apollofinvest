import numpy as np
from deap import gp
import operator
import deap.gp
import pandas as pd
df1=pd.read_csv('StockPrices/SBI/SBI.csv')
df1 = df1[['Date','Close', 'Volume', 'MarketCap', 'PriceToBook', 'EV', 'MarketCapToSales', 'ROE', 'EPS', 'DIV', 'MA','Volatility']]
c=df1.columns.values
pset = gp.PrimitiveSet("MAIN", 11)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(operator.pow,2)
pset.renameArguments(ARG0=c[1],ARG1=c[2],ARG2=c[3],ARG3=c[4],ARG4=c[5],ARG5=c[6],ARG6=c[7],ARG7=c[8],ARG8=c[9],ARG9=c[10],ARG10=c[11])
# expr=[deap.gp.Primitive object at 0x06D913F0,deap.gp.Primitive object at 0x06D913F0,deap.gp.Terminal object at 0x06D92C60]
func=gp.compile(expr=expr,pset=pset)
answer = func(Close=1, Volume=2, MarketCap=2,
                          PriceToBook=2, EV=2, MarketCapToSales=2,
                          ROE=0, EPS=2, DIV=2, MA=2,Volatility=2)
print(expr)
