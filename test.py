import pandas as pd
import os
import numpy as np
import pickle
# # Read the excel sheet to pandas dataframe
# # df1 = pd.read_csv("SBI.csv")
# # date_60=df1['Date'].values[0:48]
# # print(date_60)
# # print(df1.head())
# # col = df1.columns.values
# # print(col)
#
# # def stockRanks(func):
# #     factor_model_value=list()
# #
# #     for files in stocknamesUsers\\HP\\PycharmProjects\\untitled12\\StockPrices'):
# #         df1 = pd.read_csv("C:\\Users\\HP\\PycharmProjects\\untitled12\\StockPrices\\" + files + "\\" + files + ".csv")
# #         df1.set_index('Date', inplace=True)
# #         col=df1.columns.values
# #         for c in col:
# #             if df1[c].max()== 0 and df1[c].min()==0:
# #                 df1[c]=0
# #             elif df1[c].max()== df1[c].min():
# #                 df1[c]=1
# #             else:
# #                 df1[c] = (df1[c]-df1[c].min()) / (df1[c].max()-df1[c].min())
# #         col = df1.columns.values
# #         close=df1.ix[date,col[0]]
# #         volume=df1.ix[date,col[1]]
# #         Market=df1.ix[date,col[2]]
# #         PriceToEarn=df1.ix[date,col[3]]
# #         PriceToBook=df1.ix[date,col[4]]
# #         PriceToCash=df1.ix[date,col[5]]
# #         EV=df1.ix[date,col[6]]
# #         MarketCapToSales=df1.ix[date,col[7]]
# #         ROE=df1.ix[date,col[8]]
# #         EPS = df1.ix[date, col[9]]
# #         DIV=df1.ix[date,col[10]]
# #         answer=func(Close=close,Volume=volume,MarketCap=Market,PriceToEarn=PriceToEarn,PriceToBook=PriceToBook,PriceToCash=PriceToCash,EV=EV,MarketCapToSales=MarketCapToSales,ROE=ROE,EPS=EPS,DIV=DIV)
# #         factor_model_value.append(answer)
# #     rankdict=dict()
# #     df2=pd.Series(factor_model_value)
# #     rankStock=df2.rank(ascending=False)
# #     rankStock=rankStock-1
# #     rankStock=list(rankStock.values)
# #     stockname=stocknamesUsers\\HP\\PycharmProjects\\untitled12\\StockPrices')
# #     rankStock, stockname = zip(*sorted(zip(rankStock, stockname)))
# #     count=0
# #     for i in rankStock:
# #         rankdict[i]=stockname[count]
# #         count+=1
# #     return rankdict
#
def fitness_60(func,Cash,C_max,N_stocks,df_dict,stocknames,iter):

    stocknames=stocknames
    # Read the excel sheet to pandas dataframe


    df1 = df_dict['Britania'].copy(deep=True)
    date_60 = df1.index.values[iter*12:(iter*12+12)]
    # print(len(date_60)
    # print(date_60)
    n_stocks = 4
    counter = 0
    portfolio_weights = dict()
    portfolio_number_of_stocks = dict()
    portfolio_cash = dict()
    path = 'FMCG'
    total_stocks = len(stocknames)
    cash = 100000
    c_max = cash * 0.03
    Return = list()
    Risk = list()
    Value = list()  # stores the fund value of each month
    # assign 0.0 weights to all stocks in the portfolio
    for stocks in stocknames:
        portfolio_weights[stocks] = 0.0
        portfolio_number_of_stocks[stocks] = 0.0
        portfolio_cash[stocks] = 0.0
    counter = 0
    # start the 60 month iteration for that portfolio
    for date in date_60:
        # print("=============="+str(date)+"=============================================")
        counter += 1
        factor_model_value = list()
        # start reading each stock
        for files in stocknames:
            df1 = df_dict[files].copy(deep=True)
            df1 = df1[['Price', 'Volume', 'MarketCap', 'PE', 'PB', 'ROA', 'CurrentRatio', 'InventoryTurnover','DividendPayout','CrudePrice','GoldPrice','Inflation','Forex','GDP']]
            col = df1.columns.values
            # normalize each stock
            for c in col:
                if df1[c].max() == 0 and df1[c].min() == 0:
                    df1[c] = 0
                elif df1[c].max() == df1[c].min():
                    df1[c] = 1
                else:
                    df1[c] = (df1[c] - df1[c].min()) / (df1[c].max() - df1[c].min())
            col = df1.columns.values
            price = df1.ix[date, col[0]]
            volume = df1.ix[date, col[1]]
            Market = df1.ix[date, col[2]]
            PE = df1.ix[date, col[3]]
            PB = df1.ix[date, col[4]]
            ROA = df1.ix[date, col[5]]
            CurrentRatio = df1.ix[date, col[6]]
            Inventory = df1.ix[date, col[7]]
            Div= df1.ix[date, col[8]]
            Crude = df1.ix[date, col[9]]
            Gold= df1.ix[date, col[10]]
            Inflation= df1.ix[date, col[11]]
            Forex=df1.ix[date,col[12]]
            GDP=df1.ix[date,col[12]]
            # caculate factor model values for this stock
            answer = func(Price=price, Volume=volume, MarketCap=Market,
                          PE=PE,PB=PB,ROA=ROA,CurrentRatio=CurrentRatio,InventoryTurnover=Inventory,DividendPayout=Div,CrudePrice=Crude,GoldPrice=Gold,Inflation=Inflation,Forex=Forex,GDP=GDP)
            factor_model_value.append(answer)  # contains fmv for all stocks

        # rank and sort all stocks
        stock_names = stocknames
        list_values, list_stocks = zip(*sorted(zip(factor_model_value, stock_names), reverse=True))

        # start trading
        top_fractile = list()
        bottom_fractile = list()
        current_month = dict()
        month_end = dict()
        with open('df_dict_oc.pkl', 'rb') as f:
            df_dict_oc = pickle.load(f)
        #  current and previous months stock prices and store in dict
        for i in stocknames:
            df_oc = df_dict_oc[i].copy(deep=True)
            current_month[i] = df_oc.ix[date, df_oc.columns.values[0]]
            month_end[i] = df_oc.ix[date, df_oc.columns.values[1]]
        # calculate current months fund value
        # portfolio cash for each stock
        fund_value = 0
        # print("Cash at start" + str(cash))
        fund_value = fund_value + cash

        for i in stocknames:
            fund_value = fund_value + (current_month[i] * portfolio_number_of_stocks[i])
            portfolio_cash[i] = portfolio_number_of_stocks[i] * current_month[i]  # update cash portfolio
        fund_value_start=fund_value
        # print("Start Value")
        # print(fund_value_start)
        # store fund value globally
        c_max = fund_value * 0.03
        # print("CMAX" + str(c_max))
        # update weights

        for i in stocknames:
            portfolio_weights[i] = portfolio_cash[i] / fund_value

        # start selling
        for i in range(9, 3, -1):
            bottom_fractile.append(list_stocks[i])
        # print("Bottom Fractile")
        # print(bottom_fractile)

        for i in df_dict.keys():
            if i not in bottom_fractile and i not in list_stocks[0:4]:
                bottom_fractile.append(i)
        # print("Middle 2")
        # print(list_stocks[4:6])
        # sell the stocks in bottom fractile
        for i in bottom_fractile:
            if portfolio_weights[i] != 0.0:
                cash = cash + (current_month[i] * portfolio_number_of_stocks[i])  # add cash back to cash reserve
                portfolio_number_of_stocks[i] = 0.0
                portfolio_weights[i] = 0.0
                portfolio_cash[i] = 0.0

        # sell stocks weights more than 0 if not in top quartile to bring it till 0
        # print(portfolio_weights, "This is just inside for loop")
        for i in stocknames:


            if i in list_stocks[0:4]:
                if portfolio_weights[list_stocks[0]]>0.3 and i==list_stocks[0]:
                    # print("stock number 1")
                    extra_weight = portfolio_weights[i] - 0.3
                    extra_cash = extra_weight * fund_value
                    cash = cash + (fund_value * extra_weight)
                    portfolio_cash[i] = portfolio_cash[i] - extra_cash
                    portfolio_weights[i] = portfolio_cash[i] / fund_value
                    portfolio_number_of_stocks[i] = portfolio_number_of_stocks[i] - (extra_cash / current_month[i])
                elif portfolio_weights[list_stocks[1]]>0.28 and i==list_stocks[1]:
                    # print("stock number 2")
                    extra_weight = portfolio_weights[i] - 0.28
                    extra_cash = extra_weight * fund_value
                    cash = cash + (fund_value * extra_weight)
                    portfolio_cash[i] = portfolio_cash[i] - extra_cash
                    portfolio_weights[i] = portfolio_cash[i] / fund_value
                    portfolio_number_of_stocks[i] = portfolio_number_of_stocks[i] - (extra_cash / current_month[i])

                elif portfolio_weights[list_stocks[2]]>0.23 and i==list_stocks[2]:
                    # print("stock number 3")
                    extra_weight = portfolio_weights[i] - 0.23
                    extra_cash = extra_weight * fund_value
                    cash = cash + (fund_value * extra_weight)
                    portfolio_cash[i] = portfolio_cash[i] - extra_cash
                    portfolio_weights[i] = portfolio_cash[i] / fund_value
                    portfolio_number_of_stocks[i] = portfolio_number_of_stocks[i] - (extra_cash / current_month[i])
                elif portfolio_weights[list_stocks[3]]>0.19 and i==list_stocks[3]:
                    # print("stock number 3")
                    extra_weight = portfolio_weights[i] - 0.19
                    extra_cash = extra_weight * fund_value
                    cash = cash + (fund_value * extra_weight)
                    portfolio_cash[i] = portfolio_cash[i] - extra_cash
                    portfolio_weights[i] = portfolio_cash[i] / fund_value
                    portfolio_number_of_stocks[i] = portfolio_number_of_stocks[i] - (extra_cash / current_month[i])
        # print(portfolio_weights,"aftere for loop")
        # start buying

        # count the number of stocks in portfolio
        Sn = 0
        count1=0
        for i in stocknames:
            if portfolio_weights[i] != 0.0:
                Sn += 1
        for i in range(0, 4):
            top_fractile.append(list_stocks[i])
            if portfolio_weights[list_stocks[i]]>0.0:
                count1=count1+1

        # print("Top Fractile")
        # print(top_fractile)

        # buy stocks in top fractile which are not in the portfolio at all
        n=0
        for i in top_fractile:

            if Sn < n_stocks and cash > c_max:

                if portfolio_weights[i] == 0.0:
                    cash_ratio = (cash - c_max) / (n_stocks - Sn)

                    # if cash_ratio > (0.25 * fund_value):
                    #     cash_ratio = (0.25 * fund_value)
                    if i ==list_stocks[0]  and  cash_ratio > (0.3 * fund_value):
                        cash_ratio = (0.3 * fund_value)
                    elif i==list_stocks[1]  and  cash_ratio > (0.28 * fund_value):
                        cash_ratio = (0.28 * fund_value)
                    elif i==list_stocks[2]  and  cash_ratio > (0.23 * fund_value):
                        cash_ratio = (0.23 * fund_value)
                    elif i==list_stocks[3]  and  cash_ratio > (0.19 * fund_value):
                        cash_ratio = (0.19 * fund_value)
                    portfolio_cash[i] = cash_ratio
                    portfolio_weights[i] = cash_ratio / fund_value
                    portfolio_number_of_stocks[i] = round( cash_ratio / current_month[i])
                    cash -= cash_ratio
                    Sn += 1
        # if some fund is left ,buy the rest of stocks starting from the most attractive stock till 0.25
        # print("Cash" + str(cash))

        while (cash > c_max):
            # print("true")
            for i in top_fractile:
                # if portfolio_weights[top_fractile[0]] < portfolio_weights[top_fractile[1]]:
                #     missing_cash = fund_value * (portfolio_weights[top_fractile[1]]+1 - portfolio_weights[i])
                #     if (missing_cash > cash):
                #         missing_cash = cash
                #         portfolio_cash[i] += missing_cash
                #         portfolio_weights[i] += missing_cash / fund_value
                #         portfolio_number_of_stocks[i] += missing_cash / current_month[i]
                #         cash -= missing_cash




                ##### new code wich buy stocks till weights dont reach max and cash doesnt go below cmax
                if portfolio_weights[top_fractile[0]]<0.3:
                    missing_cash = fund_value * (0.3 - portfolio_weights[i])
                    if (missing_cash > cash):
                        missing_cash = cash
                    portfolio_cash[i] += missing_cash
                    portfolio_weights[i] += missing_cash / fund_value
                    portfolio_number_of_stocks[i] += missing_cash / current_month[i]
                    cash -= missing_cash
                elif portfolio_weights[top_fractile[1]] < 0.28:
                    missing_cash = fund_value * (0.28 - portfolio_weights[i])
                    if (missing_cash > cash):
                        missing_cash = cash
                    portfolio_cash[i] += missing_cash
                    portfolio_weights[i] += missing_cash / fund_value
                    portfolio_number_of_stocks[i] += missing_cash / current_month[i]
                    cash -= missing_cash
                elif portfolio_weights[top_fractile[2]] < 0.23:
                    missing_cash = fund_value * (0.23 - portfolio_weights[i])
                    if (missing_cash > cash):
                        missing_cash = cash
                    portfolio_cash[i] += missing_cash
                    portfolio_weights[i] += missing_cash / fund_value
                    portfolio_number_of_stocks[i] += missing_cash / current_month[i]
                    cash -= missing_cash
                elif portfolio_weights[top_fractile[3]] < 0.19:
                    missing_cash = fund_value * (0.19 - portfolio_weights[i])
                    if (missing_cash > cash):
                        missing_cash = cash
                    portfolio_cash[i] += missing_cash
                    portfolio_weights[i] += missing_cash / fund_value
                    portfolio_number_of_stocks[i] += missing_cash / current_month[i]
                    cash -= missing_cash
                else:
                    break

            ######Old Code

                # if portfolio_weights[i] < 0.25 and portfolio_weights[i] > 0.0:
                #     missing_cash = fund_value * (0.25 - portfolio_weights[i])
                #     if (missing_cash > cash):
                #         missing_cash = cash
                #     portfolio_cash[i] += missing_cash
                #     portfolio_weights[i] += missing_cash / fund_value
                #     portfolio_number_of_stocks[i] += missing_cash / current_month[i]
                #     cash -= missing_cash
        # print("Execute these buys")
        # print(portfolio_number_of_stocks)
        # print(portfolio_weights,"Last value")
        fund_value_end = 0
        fund_value_end = fund_value_end + cash
        # print(portfolio_weights,"end ones")
        for i in stocknames:
            fund_value_end = fund_value_end + (month_end[i] * portfolio_number_of_stocks[i])
        # print("End Value")
        # print(fund_value_end)
        month_return = (fund_value_end / fund_value_start) - 1
        # print(month_return,"This is month return")
        Value.append(month_return)
        # print("FUND VALUE " + str(fund_value))
        # print( "===========================================================================================================")
    #calculate Avg Risk and Avg Return of the current model
    # print(Value)
    # print(len(Value))
    # for i in range(1, len(date_60)):
    #     Return.append((Value[i] - Value[i - 1]) / Value[i - 1])
    # print(Value)
    prod=1
    Return_array=np.array(Value)
    # print(Return_array)
    RETURN=[]
    # Return_array=Return_array/100
    for ret in Return_array:
            RETURN.append(1+ret)
    for RET in RETURN:
        prod=prod*RET
    Avg_Return = prod-1
    Avg_Risk = Return_array.std()*3.46
    # print(Value[40])
    # print("Return"+str(Avg_Return))
    # print("Risk"+str(Avg_Risk))
    # print("Avg_Ret"+str(Avg_Return))
    # print("Avg Risk" + str(Avg_Risk))
    return Avg_Return,Avg_Risk


def fitness_trailing(func,Cash,C_max,N_stocks,df_dict,stocknames,iter,month):

    stocknames=stocknames
    df1 = df_dict['Britania'].copy(deep=True)
    date_60 = df1.index.values[(iter)*12+month:((iter)*12+12+month)]
    n_stocks = 4
    portfolio_weights = dict()
    portfolio_number_of_stocks = dict()
    portfolio_cash = dict()
    cash = 100000
    Value = list()  # stores the fund value of each month
    # assign 0.0 weights to all stocks in the portfolio
    for stocks in stocknames:
        portfolio_weights[stocks] = 0.0
        portfolio_number_of_stocks[stocks] = 0.0
        portfolio_cash[stocks] = 0.0
    counter = 0
    rank_corr=[]
    # start the 60 month iteration for that portfolio
    for date in date_60:
        # print("==============" + str(date) + "=============================================")
        counter += 1
        factor_model_value = list()
        # start reading each stock
        for files in stocknames:
            df1 = df_dict[files].copy(deep=True)
            df1 = df1[['Price', 'Volume', 'MarketCap', 'PE', 'PB', 'ProfitMargin', 'ROA', 'DebtEquity',
                      'CurrentRatio', 'InventoryTurnover', 'DividendPayout', 'CrudePrice', 'GoldPrice', 'Inflation',
                      'Forex', 'GDP', 'MA', 'Volatility', 'RepoRate', 'FII']]
            col = df1.columns.values
            # normalize each stock
            for c in col:
                if df1[c].max() == 0 and df1[c].min() == 0:
                    df1[c] = 0
                elif df1[c].max() == df1[c].min():
                    df1[c] = 1
                else:
                    df1[c] = (df1[c] - df1[c].min()) / (df1[c].max() - df1[c].min())
            col = df1.columns.values
            price = df1.ix[date, col[0]]
            volume = df1.ix[date, col[1]]
            Market = df1.ix[date, col[2]]
            PE = df1.ix[date, col[3]]
            PB = df1.ix[date, col[4]]
            ProfitMargin=df1.ix[date, col[5]]
            ROA = df1.ix[date, col[6]]
            DebtEquity=df1.ix[date,col[7]]
            CurrentRatio = df1.ix[date, col[8]]
            Inventory = df1.ix[date, col[9]]
            Div= df1.ix[date, col[10]]
            Crude = df1.ix[date, col[11]]
            Gold= df1.ix[date, col[12]]
            Inflation= df1.ix[date, col[13]]
            Forex=df1.ix[date,col[14]]
            GDP=df1.ix[date,col[15]]
            MA=df1.ix[date,col[16]]
            Volatility=df1.ix[date,col[17]]
            RepoRate=df1.ix[date,col[18]]
            FII=df1.ix[date, col[19]]
            # caculate factor model values for this stock
            answer = func(Price=price, Volume=volume, MarketCap=Market,
                          PE=PE,PB=PB,ProfitMargin=ProfitMargin,ROA=ROA,DebtEquity=DebtEquity,CurrentRatio=CurrentRatio,InventoryTurnover=Inventory,DividendPayout=Div,CrudePrice=Crude,GoldPrice=Gold,Inflation=Inflation,Forex=Forex,GDP=GDP,MA=MA,Volatility=Volatility,RepoRate=RepoRate,FII=FII)

            factor_model_value.append(answer)  # contains fmv for all stocks

        # rank and sort all stocks
        stock_names = stocknames
        list_values, list_stocks = zip(*sorted(zip(factor_model_value, stock_names), reverse=True))


        # start trading
        top_fractile = list()
        bottom_fractile = list()
        current_month = dict()
        month_end = dict()
        with open('df_dict_oc.pkl', 'rb') as f:
            df_dict_oc = pickle.load(f)
        # current and previous months stock prices and store in dict
        for i in stocknames:
            df_oc = df_dict_oc[i].copy(deep=True)
            current_month[i] = df_oc.ix[date, df_oc.columns.values[0]]
            month_end[i] = df_oc.ix[date, df_oc.columns.values[1]]
        # calculate current months fund value
        # portfolio cash for each stock
        fund_value = 0
        # print("Cash at start" + str(cash))
        fund_value = fund_value + cash

        for i in stocknames:
            fund_value = fund_value + (current_month[i] * portfolio_number_of_stocks[i])
            portfolio_cash[i] = portfolio_number_of_stocks[i] * current_month[i]  # update cash portfolio
        fund_value_start = fund_value
        # print("Start Value")
        # print(fund_value_start)
        # store fund value globally
        c_max = fund_value * 0.03
        # print("CMAX" + str(c_max))
        # update weights

        for i in stocknames:
            portfolio_weights[i] = portfolio_cash[i] / fund_value

        # start selling
        for i in range(9, 3, -1):
            bottom_fractile.append(list_stocks[i])
        # print("Bottom Fractile")
        # print(bottom_fractile)

        for i in df_dict.keys():
            if i not in bottom_fractile and i not in list_stocks[0:4]:
                bottom_fractile.append(i)
        # print("Middle 2")
        # print(list_stocks[4:6])
        # sell the stocks in bottom fractile
        for i in bottom_fractile:
            if portfolio_weights[i] != 0.0:
                cash = cash + (current_month[i] * portfolio_number_of_stocks[i])  # add cash back to cash reserve
                portfolio_number_of_stocks[i] = 0.0
                portfolio_weights[i] = 0.0
                portfolio_cash[i] = 0.0

        # sell stocks weights more than 0 if not in top quartile to bring it till 0
        # print(portfolio_weights, "This is just inside for loop")
        for i in stocknames:

            if i in list_stocks[0:4]:
                if portfolio_weights[list_stocks[0]] > 0.3 and i == list_stocks[0]:
                    # print("stock number 1")
                    extra_weight = portfolio_weights[i] - 0.3
                    extra_cash = extra_weight * fund_value
                    cash = cash + (fund_value * extra_weight)
                    portfolio_cash[i] = portfolio_cash[i] - extra_cash
                    portfolio_weights[i] = portfolio_cash[i] / fund_value
                    portfolio_number_of_stocks[i] = portfolio_number_of_stocks[i] - (extra_cash / current_month[i])
                elif portfolio_weights[list_stocks[1]] > 0.28 and i == list_stocks[1]:
                    # print("stock number 2")
                    extra_weight = portfolio_weights[i] - 0.28
                    extra_cash = extra_weight * fund_value
                    cash = cash + (fund_value * extra_weight)
                    portfolio_cash[i] = portfolio_cash[i] - extra_cash
                    portfolio_weights[i] = portfolio_cash[i] / fund_value
                    portfolio_number_of_stocks[i] = portfolio_number_of_stocks[i] - (extra_cash / current_month[i])

                elif portfolio_weights[list_stocks[2]] > 0.23 and i == list_stocks[2]:
                    # print("stock number 3")
                    extra_weight = portfolio_weights[i] - 0.23
                    extra_cash = extra_weight * fund_value
                    cash = cash + (fund_value * extra_weight)
                    portfolio_cash[i] = portfolio_cash[i] - extra_cash
                    portfolio_weights[i] = portfolio_cash[i] / fund_value
                    portfolio_number_of_stocks[i] = portfolio_number_of_stocks[i] - (extra_cash / current_month[i])
                elif portfolio_weights[list_stocks[3]] > 0.19 and i == list_stocks[3]:
                    # print("stock number 3")
                    extra_weight = portfolio_weights[i] - 0.19
                    extra_cash = extra_weight * fund_value
                    cash = cash + (fund_value * extra_weight)
                    portfolio_cash[i] = portfolio_cash[i] - extra_cash
                    portfolio_weights[i] = portfolio_cash[i] / fund_value
                    portfolio_number_of_stocks[i] = portfolio_number_of_stocks[i] - (extra_cash / current_month[i])
        # print(portfolio_weights,"aftere for loop")
        # start buying

        # count the number of stocks in portfolio
        Sn = 0
        count1 = 0
        for i in stocknames:
            if portfolio_weights[i] != 0.0:
                Sn += 1
        for i in range(0, 4):
            top_fractile.append(list_stocks[i])
            if portfolio_weights[list_stocks[i]] > 0.0:
                count1 = count1 + 1

        # print("Top Fractile")
        # print(top_fractile)

        # buy stocks in top fractile which are not in the portfolio at all
        n = 0
        for i in top_fractile:

            if Sn < n_stocks and cash > c_max:

                if portfolio_weights[i] == 0.0:
                    cash_ratio = (cash - c_max) / (n_stocks - Sn)

                    # if cash_ratio > (0.25 * fund_value):
                    #     cash_ratio = (0.25 * fund_value)
                    if i == list_stocks[0] and cash_ratio > (0.3 * fund_value):
                        cash_ratio = (0.3 * fund_value)
                    elif i == list_stocks[1] and cash_ratio > (0.28 * fund_value):
                        cash_ratio = (0.28 * fund_value)
                    elif i == list_stocks[2] and cash_ratio > (0.23 * fund_value):
                        cash_ratio = (0.23 * fund_value)
                    elif i == list_stocks[3] and cash_ratio > (0.19 * fund_value):
                        cash_ratio = (0.19 * fund_value)
                    portfolio_cash[i] = cash_ratio
                    portfolio_weights[i] = cash_ratio / fund_value
                    portfolio_number_of_stocks[i] = round(cash_ratio / current_month[i])
                    cash -= cash_ratio
                    Sn += 1
        # if some fund is left ,buy the rest of stocks starting from the most attractive stock till 0.25
        # print("Cash" + str(cash))

        while (cash > c_max):
            # print("true")
            # if portfolio_weights[top_fractile[0]] < portfolio_weights[top_fractile[1]]:
            #     missing_cash = fund_value * (portfolio_weights[top_fractile[1]]+1 - portfolio_weights[i])
            #     if (missing_cash > cash):
            #         missing_cash = cash
            #         portfolio_cash[i] += missing_cash
            #         portfolio_weights[i] += missing_cash / fund_value
            #         portfolio_number_of_stocks[i] += missing_cash / current_month[i]
            #         cash -= missing_cash




            ##### new code wich buy stocks till weights dont reach max and cash doesnt go below cmax
            if portfolio_weights[top_fractile[0]]<0.3:
                missing_cash = fund_value * (0.3 - portfolio_weights[top_fractile[0]])
                if (missing_cash > cash):
                    missing_cash = cash
                portfolio_cash[top_fractile[0]] += missing_cash
                portfolio_weights[top_fractile[0]] += missing_cash / fund_value
                portfolio_number_of_stocks[top_fractile[0]] += missing_cash / current_month[top_fractile[0]]
                cash -= missing_cash
            elif portfolio_weights[top_fractile[1]] < 0.28:
                missing_cash = fund_value * (0.28 - portfolio_weights[top_fractile[1]])
                if (missing_cash > cash):
                    missing_cash = cash
                portfolio_cash[top_fractile[1]] += missing_cash
                portfolio_weights[top_fractile[1]] += missing_cash / fund_value
                portfolio_number_of_stocks[top_fractile[1]] += missing_cash / current_month[top_fractile[1]]
                cash -= missing_cash
            elif portfolio_weights[top_fractile[2]] < 0.23:
                missing_cash = fund_value * (0.23 - portfolio_weights[top_fractile[2]])
                if (missing_cash > cash):
                    missing_cash = cash
                portfolio_cash[top_fractile[2]] += missing_cash
                portfolio_weights[top_fractile[2]] += missing_cash / fund_value
                portfolio_number_of_stocks[top_fractile[2]] += missing_cash / current_month[top_fractile[2]]
                cash -= missing_cash
            elif portfolio_weights[top_fractile[3]] < 0.19:
                missing_cash = fund_value * (0.19 - portfolio_weights[top_fractile[3]])
                if (missing_cash > cash):
                    missing_cash = cash
                portfolio_cash[top_fractile[3]] += missing_cash
                portfolio_weights[top_fractile[3]] += missing_cash / fund_value
                portfolio_number_of_stocks[top_fractile[3]] += missing_cash / current_month[top_fractile[3]]
                cash -= missing_cash
            else:
                break

                ######Old Code

                # if portfolio_weights[i] < 0.25 and portfolio_weights[i] > 0.0:
                #     missing_cash = fund_value * (0.25 - portfolio_weights[i])
                #     if (missing_cash > cash):
                #         missing_cash = cash
                #     portfolio_cash[i] += missing_cash
                #     portfolio_weights[i] += missing_cash / fund_value
                #     portfolio_number_of_stocks[i] += missing_cash / current_month[i]
                #     cash -= missing_cash
        # print("Execute these buys")
        # print(portfolio_number_of_stocks)
        # print(portfolio_weights, "Last value")
        fund_value_end = 0
        fund_value_end = fund_value_end + cash
        # print(portfolio_weights,"end ones")
        portfolio_cash_end = dict()
        portfolio_cash_start = dict()
        portfolio_returns=dict()
        for i in stocknames:
            fund_value_end = fund_value_end + (month_end[i] * portfolio_number_of_stocks[i])
            portfolio_cash_end[i] = month_end[i] * portfolio_number_of_stocks[i]
            portfolio_cash_start[i] = current_month[i] * portfolio_number_of_stocks[i]
        # print("End Value")
        # print(fund_value_end)
        returns_list=[]
        for i in stocknames:
            portfolio_returns[i] = (month_end[i] / current_month[i]) - 1
            returns_list.append(portfolio_returns[i])
        # print("Cash per stock at the start")
        # print(portfolio_cash_start)
        # print("Cash per stock at the end")
        # print(portfolio_cash_end)
        # print("Returns per stock")
        # print(portfolio_returns)
        month_return = (fund_value_end / fund_value_start) - 1
        # print(month_return,"This is month return")
        Value.append(month_return)
        # print("FUND VALUE " + str(fund_value))
        # print( "===========================================================================================================")
        # calculate Avg Risk and Avg Return of the current model
        # print(Value)
        # print(len(Value))
        # for i in range(1, len(date_60)):
        #     Return.append((Value[i] - Value[i - 1]) / Value[i - 1])
        # print(Value)
        # rank_corr.append(spearmanr(factor_model_value, returns_list))
    # rank_mean=np.mean(rank_corr)
    prod = 1
    Return_array = np.array(Value)
    # print(Return_array)
    RETURN = []
    # Return_array=Return_array/100
    for ret in Return_array:
        RETURN.append(1 + ret)
    for RET in RETURN:
        prod = prod * RET
    Avg_Return = prod - 1
    Avg_Risk = Return_array.std() * 3.46
    # print(Value[40])
    # print("Return" + str(Avg_Return))
    # print("Risk" + str(Avg_Risk))
    # print("Avg_Ret"+str(Avg_Return))
    # print("Avg Risk" + str(Avg_Risk))
    return Avg_Return, Avg_Risk












