import os
import pandas as pd
for files in os.listdir("StockPrices"):
    df = pd.read_csv("StockPrices\\" + files + "\\" + files + ".csv")
    df.set_index('Date', inplace=True)
    # print(df.columns.values)
    df=df[['Close' ,'Volume' ,'Market Cap' ,'PriceToBook' ,'EV' ,'MarketCapToSales', 'ROE' ,'EPS' ,'DIV' ,'MA']]
    print(df.columns.values)
    break