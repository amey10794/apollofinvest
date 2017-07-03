import pandas as pd
from pandas import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
df=pd.read_csv("StockPrices//SBI//SBI.csv")
df.set_index('Date',inplace=True)
df = df[['Close']]
def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')
# plt.plot(df.index,df['Close'])
# plt.show()