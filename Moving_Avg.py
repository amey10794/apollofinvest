import pandas as pd
import numpy as np
import os
# # Read the excel sheet to pandas dataframe
# df1 = pd.read_csv("StockPrices//AsianPaints//AsianPaints_Daily.csv")
# df1=df1[['Date','Close Price']]
# df1['Date']=pd.to_datetime(df1['Date'])
# df1=df1.sort_values(by='Date')
# df1.set_index('Date',inplace=True)
# df1=df1.dropna()
# df1['MA']=df1.rolling(window=30,center=False).mean()
# print(df1[250:].head)
# dates_daily=df1.index.values
# # print(str(dates_daily[0])[0:4]+str(dates_daily[0])[5:7])
# df2=pd.read_csv("StockPrices//AsianPaints//AsianPaints.csv")
# df2.set_index('Date',inplace=True)
# dates=df2.index.values
# # print(dates)
# # print(df2.tail())
# MA_Values=[]
# # print(MA_Values)
# # for date in dates:
# #     MA_Values=[]
# #     for date in range(len(dates_daily)):
# #         dates_daily_trimmed=str(dates_daily[i])
# #         dates_daily_trimmed=(dates_daily_trimmed[0:4]+ dates_daily_trimmed[5:7])
# #         date=str(int(date))
# #         if date == dates_daily_trimmed:
# #             df1.ix[date,'MA']=1
# #
for files in os.listdir('StockPrices'):
        print("======================"+files+"============================================")
        df2 = pd.read_csv("StockPrices//"+files+"//"+files+"_Daily.csv")
        df2 = df2[['Date', 'Close Price']]
        df2['Date'] = pd.to_datetime(df2['Date'])
        df2 = df2.sort_values(by='Date')
        df2.set_index('Date', inplace=True)
        df2 = df2.dropna()
        df2['MA'] = df2.rolling(window=30, center=False).mean()
        dates_daily = df2.index.values
        df1 = pd.read_csv("StockPrices//"+files+"//"+files+".csv")
        df1.set_index('Date', inplace=True)
        dates = df1.index.values
        for date in dates:
            for date_daily in dates_daily:
                date_daily_trimmed=str(date_daily)[0:4]+str(date_daily)[5:7]
                date_trimmed=str(int(date))
                if date_trimmed == date_daily_trimmed:
                    df1.ix[date,'MA']=df2.get_value(date_daily,'MA')
        file_name = files + ".csv"
        df1.to_csv('StockPrices\\' + files + '\\' + file_name)
