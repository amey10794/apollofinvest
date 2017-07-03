import pandas as pd
df=pd.read_csv('Forex.csv')
df.set_index('Date',inplace=True)
df['Forex']=(df['Bid']+df['Ask'])/2
print(df.head())
df.to_excel("Forex.xlsx")