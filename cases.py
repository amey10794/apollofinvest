import pandas as pd
import os
path='C:\\Users\\HP\\PycharmProjects\\untitled12\\StockPrices'
df_dict=dict()
for i in os.listdir(path):
    for files in os.listdir('C:\\Users\\HP\\PycharmProjects\\untitled12\\StockPrices'):
        df=pd.read_csv("C:\\Users\\HP\\PycharmProjects\\untitled12\\StockPrices\\" + files + "\\" + files + ".csv")
        df_dict[files]=df

for i in os.listdir(path):
    print(df_dict[i].head())



