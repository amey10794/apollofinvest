import pandas as pd

# Read the excel sheet to pandas dataframe
df1 = pd.read_excel("MRF.xlsx", sheetname=0)
df1=df1[['Date','Close','Volume','Market Cap']]
df1.set_index('Date',inplace=True)
df1=df1.dropna()
print(df1.head())

# Read the excel sheet to pandas dataframe
df2 = pd.read_excel("MRF_Ratios.xlsx", sheetname=0)
df2.set_index('Year',inplace=True)
df2=df2[[0,1,2,3,4,5]]
print(df2)
print("================================================================")
df3 = pd.read_excel("Volatility.xlsx", sheetname=0)
df3=df3[['Date','Close']]
df3.set_index('Date',inplace=True)
df3=df3.dropna()
df3['Volatility']=df3.pct_change()
print(df3.head())
print("================================================================")

for year in df2.index:
    for date in df1.index:
        if(str(date)[2:4] == str(year).strip()):
            print("True")
            df1.ix[date,'PE']=df2.get_value(year,df2.columns[0])
            df1.ix[date,'PB']=df2.get_value(year,df2.columns[1])
            df1.ix[date,'EPS']=df2.get_value(year,df2.columns[2])
            df1.ix[date,'ROE']=df2.get_value(year,df2.columns[3])
            df1.ix[date,'Div Yield']=df2.get_value(year,df2.columns[4])
            df1.ix[date, 'Debt To Equity'] = df2.get_value(year, df2.columns[5])

        else:
            pass
            # print(str(date)[2:4])
            # print(str(year).strip())
            # print("False")
            # #df1['PE'] = (df2.get_value(year, df2.columns[0]))
print(df1)
