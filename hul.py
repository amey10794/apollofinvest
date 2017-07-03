import pandas as pd
import os
import numpy as np


def func(Close, Volume, MarketCap, PriceToBook, EV, MarketCapToSales, ROE, EPS, DIV,MA,Volatility):
    return ((Close + Volume) * MarketCapToSales + (PriceToBook + EV) -  MA)

path='StockPrices'
df_dict=dict()
for i in os.listdir(path):
    for files in os.listdir(path):
        df=pd.read_csv("StockPrices\\" + files + "\\" + files + ".csv")
        df.set_index('Date',inplace=True)
        df_dict[files]=df

# Read the excel sheet to pandas dataframe
df1 = df_dict['SBI']
date_60=df1.index.values
print(len(date_60))
#print(date_60)
n_stocks=4
counter=0
portfolio_weights=dict()
portfolio_number_of_stocks=dict()
portfolio_cash=dict()
stocknames=os.listdir(path)
total_stocks=len(os.listdir(path))
cash = 100000
c_max = cash*0.03
Return=list()
Risk=list()
Value=list() #stores the fund value of each month
#assign 0.0 weights to all stocks in the portfolio
for stocks in stocknames:
    portfolio_weights[stocks]= 0.0
    portfolio_number_of_stocks[stocks]=0.0
    portfolio_cash[stocks]=0.0
counter=0
#start the 60 month iteration for that portfolio
for date in date_60:
    print("======================================="+str(counter)+"========================================")
    counter+=1
    factor_model_value = list()
    #start reading each stock
    for files in os.listdir(path):
        df1 = df_dict[files].copy(deep=True)
        df = df[['Close', 'Volume', 'Market Cap', 'PriceToBook', 'EV', 'MarketCapToSales', 'ROE', 'EPS', 'DIV', 'MA','Volatility']]
        col = df1.columns.values
        #normalize each stock
        for c in col:
            if df1[c].max() == 0 and df1[c].min() == 0:
                df1[c] = 0
            elif df1[c].max() == df1[c].min():
                df1[c] = 1
            else:
                df1[c] = (df1[c] - df1[c].min()) / (df1[c].max() - df1[c].min())
        print(df1.head())
        col = df1.columns.values
        close = df1.ix[date, col[0]]
        volume = df1.ix[date, col[1]]
        Market = df1.ix[date, col[2]]
        PriceToBook = df1.ix[date, col[3]]
        EV = df1.ix[date, col[4]]
        MarketCapToSales = df1.ix[date, col[5]]
        ROE = df1.ix[date, col[6]]
        EPS = df1.ix[date, col[7]]
        DIV = df1.ix[date, col[8]]
        MA=df1.ix[date,col[9]]
        Volatility=df1.ix[date,col[10]]
        #['Close' 'Volume' 'Market Cap' 'PriceToBook' 'EV' 'MarketCapToSales' 'ROE' 'EPS' 'DIV' 'MA']
        # caculate factor model values for this stock
        answer = func(Close=close, Volume=volume, MarketCap=Market,
                      PriceToBook=PriceToBook, EV=EV, MarketCapToSales=MarketCapToSales,
                      ROE=ROE, EPS=EPS, DIV=DIV,MA=MA,Volatility=Volatility)
        factor_model_value.append(answer) #contains fmv for all stocks

    #rank and sort all stocks
    stock_names=os.listdir(path)
    list_values, list_stocks = zip(*sorted(zip(factor_model_value, stock_names),reverse=True))

    #start trading
    top_fractile=list()
    bottom_fractile=list()
    current_month=dict()
    previous_month=dict()

    #  current and previous months stock prices and store in dict
    for i in os.listdir(path):
        df1 = df_dict[i]
        current_month[i]=df1.ix[date, df1.columns.values[0]]
    # calculate current months fund value
    # portfolio cash for each stock
    # print("9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999")
    # print(current_month)
    fund_value=0
    print("Cash at start"+str(cash))
    fund_value=fund_value+cash

    for i in os.listdir(path):
        fund_value=fund_value+(current_month[i]*portfolio_number_of_stocks[i])
        portfolio_cash[i]=portfolio_number_of_stocks[i]*current_month[i]  # update cash portfolio

    #store fund value globally
    Value.append(fund_value)
    c_max=fund_value*0.03
    print("CMAX"+str(c_max))
    # update weights
    for i in os.listdir(path):
        portfolio_weights[i]=portfolio_cash[i]/fund_value

    # start selling
    for i in range(9,5,-1):
        bottom_fractile.append(list_stocks[i])
    print("Bottom Fractile")
    print(bottom_fractile)

    # sell the stocks in bottom fractile
    for i in bottom_fractile:
        if portfolio_weights[i]!=0.0:
            cash=cash+(current_month[i]*portfolio_number_of_stocks[i]) #add cash back to cash reserve
            portfolio_number_of_stocks[i]=0.0
            portfolio_weights[i]=0.0
            portfolio_cash[i]=0.0

    # sell stocks weights more than 0.25 to bring it till 0.25
    for i in os.listdir(path):
        if portfolio_weights[i]>0.25:
            extra_weight = portfolio_weights[i] - 0.25
            extra_cash=extra_weight*fund_value
            cash = cash + (fund_value * extra_weight)
            portfolio_cash[i]=portfolio_cash[i]-extra_cash
            portfolio_weights[i]=portfolio_cash[i]/fund_value
            portfolio_number_of_stocks[i]=portfolio_number_of_stocks[i]-(extra_cash/current_month[i])

    # start buying

    # count the number of stocks in portfolio
    Sn = 0
    for i in os.listdir(path):
        if portfolio_weights[i] != 0.0:
            Sn+=1
    for i in range(0, 4):
        top_fractile.append(list_stocks[i])
    print("Top Fractile")
    print(top_fractile)

    # buy stocks in top fractile which are not in the portfolio at all
    for i in top_fractile:
        if Sn<n_stocks and cash > c_max:
            if portfolio_weights[i] == 0.0 :
                cash_ratio = (cash - c_max) / (n_stocks - Sn)
                if cash_ratio > (0.25 * fund_value):
                    cash_ratio = (0.25 * fund_value)
                portfolio_cash[i] = cash_ratio
                portfolio_weights[i] = cash_ratio / fund_value
                portfolio_number_of_stocks[i] = cash_ratio / current_month[i]
                cash -= cash_ratio


    # if some fund is left ,buy the rest of stocks starting from the most attractive stock till 0.25
    print(portfolio_weights)
    print("Cash"+ str(cash))
    while (cash>c_max):
        print("true")
        for i in list_stocks:
            if portfolio_weights[i]<0.25 and portfolio_weights[i]>0:
                missing_cash = fund_value*(0.25-portfolio_weights[i])
                if (missing_cash>cash):
                    missing_cash=cash
                portfolio_cash[i] += missing_cash
                portfolio_weights[i] += missing_cash / fund_value
                portfolio_number_of_stocks[i] += missing_cash / current_month[i]
                cash -= missing_cash
    print("FUND VALUE " + str(fund_value))
    print("===========================================================================================================")
# calculate Avg Risk and Avg Return of the current model
for i in range(1,len(date_60)):
    Return.append((Value[i]-Value[i-1])/Value[i-1])

Return_array=np.array(Return)
Avg_Return=Return_array.mean()
Avg_Risk=Return_array.std()

print(Avg_Risk)
print(Avg_Return)





