import pandas as pd
import numpy as np
df_test=pd.read_excel("Test.xlsx",sheetname=0)
df_test.set_index('Date',inplace=True)
for i in range(len(df_test.index)):
    date = df_test.index[i]
    if i!=0:

        df_test.ix[date,'Vol']=df_test.get_value(date,'Close Price')/df_test.get_value(df_test.index[i-1],'Close Price')-1

    else:
        df_test.ix[date, 'Vol'] = 0
df_test['MA']=df_test['Close Price'].rolling(center=False,window=15).mean()
print(df_test)