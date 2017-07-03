import pandas as pd
import numpy as np
import os
# Read the excel sheet to pandas dataframe
df1 = pd.read_csv("StockPrices//AsianPaints//AsianPaints_Daily.csv")
df1=df1[['Date','Close Price']]
df1['Date']=pd.to_datetime(df1['Date'])
df1['Date'] = df1['Date'].dt.strftime('%Y%m%d')

df1=df1.sort_values(by='Date')
df1.set_index('Date',inplace=True)

dates_daily=df1.index.values

# df1.set_index('Date',inplace=True)
for i in range(len(dates_daily)):
    if(i==0):
        df1.ix[dates_daily[i],'Volatility']=float('NaN')
    else:
        df1.ix[i,'Volatility']=(df1.ix[dates_daily[i],'Close Price']/df1.ix[dates_daily[i-1],'Close Price']) -1
df2=pd.read_csv("StockPrices//AsianPaints//AsianPaints.csv")
df2.set_index('Date',inplace=True)

datas1=df2.index.values
df1=df1[['Volatility']]
for files in os.listdir('StockPrices'):
    print("============================"+files+"========================")
    df1 = pd.read_csv("StockPrices//"+files+"//"+files+"_Daily.csv")
    df1 = df1[['Date', 'Close Price']]
    df1['Date'] = pd.to_datetime(df1['Date'])
    df1['Date'] = df1['Date'].dt.strftime('%Y%m%d')
    df1 = df1.sort_values(by='Date')
    df1.set_index('Date', inplace=True)
    dates_daily = df1.index.values
    # df1.set_index('Date',inplace=True)
    for i in range(len(dates_daily)):
        if (i == 0):
            df1.ix[dates_daily[i], 'Volatility'] = float('NaN')
        else:
            df1.ix[i, 'Volatility'] = (df1.ix[dates_daily[i], 'Close Price'] / df1.ix[dates_daily[i - 1], 'Close Price']) - 1
    df2 = pd.read_csv("StockPrices//"+files+"//"+files+".csv")
    df2.set_index('Date', inplace=True)
    datas1 = df2.index.values
    df1 = df1[['Volatility']]
    for date in datas1:
        vol=[]
        for date_daily in dates_daily:
            date_daily_trimmed= str(date_daily)[0:4]+str(date_daily)[4:6]
            date_trimmed= str(int(date))
            if date_trimmed==date_daily_trimmed:
                vol.append(df1.get_value(date_daily,'Volatility'))
        arr=np.array(vol)
        df2.ix[date,'Volatility']=arr.mean()
    file_name = files + ".csv"
    df2.to_csv('StockPrices\\' + files + '\\' + file_name)




