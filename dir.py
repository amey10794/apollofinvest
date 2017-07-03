import os
import pandas as pd
stocks=[]
for files in os.listdir('C:\\Users\\HP\\PycharmProjects\\untitled12\\StockPrices'):
    print("=================="+files+"==========================")
    xl_stock='C:\\Users\\HP\\PycharmProjects\\untitled12\\StockPrices\\'+files+'\\'+files+'_Stock.xlsx'
    stocks.append(xl_stock)
    df1 = pd.read_excel(xl_stock,sheetname=0)
    df1 = df1[['Date', 'Close', 'Volume', 'Market Cap']]
    df1.set_index('Date', inplace=True)
    df1 = df1.dropna()
    xl_ratio = 'C:\\Users\\HP\\PycharmProjects\\untitled12\\StockPrices\\' + files + '\\' + files + '_Ratio.xlsx'
    df2 = pd.read_excel(xl_ratio, sheetname=0)
    df2.set_index('Year', inplace=True)
    df2 = df2.dropna()
    for year in df2.index:
        for date in df1.index:
            if (str(date)[2:4] == str(year).strip()):
                df1.ix[date, 'PriceToEarn'] = df2.get_value(year, df2.columns[0])
                df1.ix[date, 'PriceToBook'] = df2.get_value(year, df2.columns[1])
                df1.ix[date, 'PriceToCash'] = df2.get_value(year, df2.columns[2])
                df1.ix[date, 'EV'] = df2.get_value(year, df2.columns[3])
                df1.ix[date, 'MarketCapToSales'] = df2.get_value(year, df2.columns[4])
                df1.ix[date, 'ROE'] = df2.get_value(year, df2.columns[5])
                df1.ix[date, 'EPS'] = df2.get_value(year, df2.columns[6])
                df1.ix[date, 'DIV'] = df2.get_value(year, df2.columns[7])

            else:
                pass
                # print(str(date)[2:4])
                # print(str(year).strip())
                # print("False")
                # #df1['PE'] = (df2.get_value(year, df2.columns[0]))

    df1.dropna(inplace=True)
    df1=df1.iloc[::-1]
    file_name=files+".csv"
    df1.to_csv('C:\\Users\\HP\\PycharmProjects\\untitled101\\StockPrices\\' + files + '\\' +file_name)
    print(df1.head())