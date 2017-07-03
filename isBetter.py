import pandas as pd
import numpy as np
import pickle
import os

def probability(func,df_dict,iter):

    path = 'FMCG'
    stocknames = os.listdir(path)
    # Read the excel sheet to pandas dataframe
    df1 = df_dict['Britania'].copy(deep=True)
    date_60 = df1.index.values[0:iter*12+12]

    # print(len(date_60))

    # print(date_60)
    n_stocks = 4
    # counter = 0
    portfolio_weights = dict()
    portfolio_number_of_stocks = dict()
    portfolio_cash = dict()
    # path = 'StockPrices'
    # total_stocks = len(stocknames)
    cash = 100000
    # c_max = cash * 0.03
    Return = list()
    index_return = list()
    # Risk = list()
    Value = list()  # stores the fund value of each month
    Ind_Value = list()
    # assign 0.0 weights to all stocks in the portfolio
    for stocks in stocknames:
        portfolio_weights[stocks] = 0.0
        portfolio_number_of_stocks[stocks] = 0.0
        portfolio_cash[stocks] = 0.0
    # counter = 0
    # start the N month iteration for that portfolio
    for date in date_60:
        # print("=============="+str(counter))
        # counter += 1
        factor_model_value = list()
        # start reading each stock
        for files in stocknames:
            df1 = df_dict[files].copy(deep=True)
            df1 = df1[['Date', 'Price', 'Volume', 'MarketCap', 'PE', 'PB', 'ProfitMargin', 'ROA', 'DebtToEquity',
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
            DebtToEquity=df1.ix[date,col[7]]
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
                          PE=PE,PB=PB,ProfitMargin=ProfitMargin,ROA=ROA,DebtToEquity=DebtToEquity,CurrentRatio=CurrentRatio,InventoryTurnover=Inventory,DividendPayout=Div,CrudePrice=Crude,GoldPrice=Gold,Inflation=Inflation,Forex=Forex,GDP=GDP,MA=MA,Volatility=Volatility,RepoRate=RepoRate,FII=FII)

            factor_model_value.append(answer)  # contains fmv for all stocks


        # rank and sort all stocks
        stock_names = stocknames
        list_values, list_stocks = zip(*sorted(zip(factor_model_value, stock_names), reverse=True))

        # start trading
        top_fractile = list()
        bottom_fractile = list()
        current_month = dict()
        previous_month = dict()

        #  current and previous months stock prices and store in dict
        for i in stocknames:
            df1 = df_dict[i].copy(deep=True)
            current_month[i] = df1.ix[date, df1.columns.values[0]]
        # calculate current months fund value
        # portfolio cash for each stock
        fund_value = 0
        index_value = 0  # value of a portfolio containing all possible stocks distributed equally
        # print("Cash at start" + str(cash))
        fund_value = fund_value + cash

        for i in stocknames:
            fund_value = fund_value + (current_month[i] * portfolio_number_of_stocks[i])
            index_value = index_value + (current_month[i]) * 0.1
            portfolio_cash[i] = portfolio_number_of_stocks[i] * current_month[i]  # update cash portfolio

        # store fund value globally
        Value.append(fund_value)
        Ind_Value.append(index_value)
        c_max = fund_value * 0.03
        # print("CMAX" + str(c_max))
        # update weights
        for i in stocknames:
            portfolio_weights[i] = portfolio_cash[i] / fund_value

        # start selling
        for i in range(9, 5, -1):
            bottom_fractile.append(list_stocks[i])
        # print("Bottom Fractile")
        # print(bottom_fractile)

        # sell the stocks in bottom fractile
        for i in bottom_fractile:
            if portfolio_weights[i] != 0.0:
                cash = cash + (current_month[i] * portfolio_number_of_stocks[i])  # add cash back to cash reserve
                portfolio_number_of_stocks[i] = 0.0
                portfolio_weights[i] = 0.0
                portfolio_cash[i] = 0.0

        # sell stocks weights more than 0.25 to bring it till 0.25
        for i in stocknames:
            if portfolio_weights[i] > 0.25:
                extra_weight = portfolio_weights[i] - 0.25
                extra_cash = extra_weight * fund_value
                cash = cash + (fund_value * extra_weight)
                portfolio_cash[i] = portfolio_cash[i] - extra_cash
                portfolio_weights[i] = portfolio_cash[i] / fund_value
                portfolio_number_of_stocks[i] = portfolio_number_of_stocks[i] - (extra_cash / current_month[i])

        # start buying

        # count the number of stocks in portfolio
        Sn = 0
        for i in stocknames:
            if portfolio_weights[i] != 0.0:
                Sn += 1
        for i in range(0, 4):
            top_fractile.append(list_stocks[i])
        # print("Top Fractile")
        # print(top_fractile)

        # buy stocks in top fractile which are not in the portfolio at all
        for i in top_fractile:
            if Sn < n_stocks and cash > c_max:
                if portfolio_weights[i] == 0.0:
                    cash_ratio = (cash - c_max) / (n_stocks - Sn)
                    if cash_ratio > (0.25 * fund_value):
                        cash_ratio = (0.25 * fund_value)
                    portfolio_cash[i] = cash_ratio
                    portfolio_weights[i] = cash_ratio / fund_value
                    portfolio_number_of_stocks[i] = cash_ratio / current_month[i]
                    cash -= cash_ratio

        # if some fund is left ,buy the rest of stocks starting from the most attractive stock till 0.25
        # print(portfolio_weights)
        # print("Cash" + str(cash))
        while (cash > c_max):
            # print("true")
            for i in list_stocks:
                if portfolio_weights[i] < 0.25 and portfolio_weights[i] > 0:
                    missing_cash = fund_value * (0.25 - portfolio_weights[i])
                    if (missing_cash > cash):
                        missing_cash = cash
                    portfolio_cash[i] += missing_cash
                    portfolio_weights[i] += missing_cash / fund_value
                    portfolio_number_of_stocks[i] += missing_cash / current_month[i]
                    cash -= missing_cash
                    # print("FUND VALUE " + str(fund_value))
                    # print( "===========================================================================================================")
    # calculate Avg Risk and Avg Return of the current model
    # print(Value)
    # print(len(Value))
    # print(Value)
    # print(Ind_Value)
    # print(len(Ind_Value))
    for i in range(1, len(date_60)):
        Return.append((Value[i] - Value[i - 1]) / Value[i - 1])
        index_return.append((Ind_Value[i] - Ind_Value[i - 1]) / Ind_Value[i - 1])
    numerator = 0
    denominator = len(date_60)
    for i in range(len(Return)):
        if (Return[i] > index_return[i]):
            numerator += 1

    probability = numerator / denominator
    # print(probability)
    # Return_array = np.array(Return)
    # Avg_Return = Return_array.mean() * 12
    # Avg_Risk = Return_array.std() * 3.46
    # print(Value[40])
    return probability
def trailing_probability(func,df_dict,iter,month):
    # print("Entered trailing prob")
    path = 'FMCG'
    stocknames = os.listdir(path)
    # Read the excel sheet to pandas dataframe
    df1 = df_dict['Britania'].copy(deep=True)
    date_60 = df1.index.values[0:iter*12+12+month]
    # for date in date_60:
    #     print(date)
    # print(len(date_60))

    # print(date_60)
    n_stocks = 4
    # counter = 0
    portfolio_weights = dict()
    portfolio_number_of_stocks = dict()
    portfolio_cash = dict()
    # path = 'StockPrices'
    # total_stocks = len(stocknames)
    cash = 100000
    # c_max = cash * 0.03
    Return = list()
    index_return = list()
    # Risk = list()
    Value = list()  # stores the fund value of each month
    Ind_Value = list()
    # assign 0.0 weights to all stocks in the portfolio
    for stocks in stocknames:
        portfolio_weights[stocks] = 0.0
        portfolio_number_of_stocks[stocks] = 0.0
        portfolio_cash[stocks] = 0.0
    # counter = 0
    # start the N month iteration for that portfolio
    for date in date_60:
        # print("=============="+str(date))
        # counter += 1
        factor_model_value = list()
        # start reading each stock
        for files in stocknames:
            df1 = df_dict[files].copy(deep=True)
            df1 = df1[['Price', 'Volume', 'MarketCap', 'PE', 'PB', 'ProfitMargin', 'ROA', 'DebtEquity',
                       'CurrentRatio', 'InventoryTurnover', 'DividendPayout', 'CrudePrice', 'GoldPrice', 'Inflation',
                       'Forex', 'GDP', 'MA', 'Volatility', 'RepoRate', 'FII']]
            # df1 = df1[['Price', 'Volume', 'MarketCap', 'PE', 'PB', 'ROA', 'CurrentRatio', 'InventoryTurnover','DividendPayout','CrudePrice','GoldPrice','Inflation','Forex','GDP']]
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
            ProfitMargin = df1.ix[date, col[5]]
            ROA = df1.ix[date, col[6]]
            DebtEquity = df1.ix[date, col[7]]
            CurrentRatio = df1.ix[date, col[8]]
            Inventory = df1.ix[date, col[9]]
            Div = df1.ix[date, col[10]]
            Crude = df1.ix[date, col[11]]
            Gold = df1.ix[date, col[12]]
            Inflation = df1.ix[date, col[13]]
            Forex = df1.ix[date, col[14]]
            GDP = df1.ix[date, col[15]]
            MA = df1.ix[date, col[16]]
            Volatility = df1.ix[date, col[17]]
            RepoRate = df1.ix[date, col[18]]
            FII = df1.ix[date, col[19]]
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
        previous_month = dict()

        #  current and previous months stock prices and store in dict
        for i in stocknames:
            df1 = df_dict[i].copy(deep=True)
            current_month[i] = df1.ix[date, df1.columns.values[0]]
        # calculate current months fund value
        # portfolio cash for each stock
        fund_value = 0
        index_value = 0  # value of a portfolio containing all possible stocks distributed equally
        # print("Cash at start" + str(cash))
        fund_value = fund_value + cash

        for i in stocknames:
            fund_value = fund_value + (current_month[i] * portfolio_number_of_stocks[i])
            index_value = index_value + (current_month[i]) * 0.1
            portfolio_cash[i] = portfolio_number_of_stocks[i] * current_month[i]  # update cash portfolio

        # store fund value globally
        Value.append(fund_value)
        Ind_Value.append(index_value)
        c_max = fund_value * 0.03
        # print("CMAX" + str(c_max))
        # update weights
        for i in stocknames:
            portfolio_weights[i] = portfolio_cash[i] / fund_value

        # start selling
        for i in range(9, 5, -1):
            bottom_fractile.append(list_stocks[i])
        # print("Bottom Fractile")
        # print(bottom_fractile)

        # sell the stocks in bottom fractile
        for i in bottom_fractile:
            if portfolio_weights[i] != 0.0:
                cash = cash + (current_month[i] * portfolio_number_of_stocks[i])  # add cash back to cash reserve
                portfolio_number_of_stocks[i] = 0.0
                portfolio_weights[i] = 0.0
                portfolio_cash[i] = 0.0

        # sell stocks weights more than 0.25 to bring it till 0.25
        for i in stocknames:
            if portfolio_weights[i] > 0.25:
                extra_weight = portfolio_weights[i] - 0.25
                extra_cash = extra_weight * fund_value
                cash = cash + (fund_value * extra_weight)
                portfolio_cash[i] = portfolio_cash[i] - extra_cash
                portfolio_weights[i] = portfolio_cash[i] / fund_value
                portfolio_number_of_stocks[i] = portfolio_number_of_stocks[i] - (extra_cash / current_month[i])

        # start buying

        # count the number of stocks in portfolio
        Sn = 0
        for i in stocknames:
            if portfolio_weights[i] != 0.0:
                Sn += 1
        for i in range(0, 4):
            top_fractile.append(list_stocks[i])
        # print("Top Fractile")
        # print(top_fractile)

        # buy stocks in top fractile which are not in the portfolio at all
        for i in top_fractile:
            if Sn < n_stocks and cash > c_max:
                if portfolio_weights[i] == 0.0:
                    cash_ratio = (cash - c_max) / (n_stocks - Sn)
                    if cash_ratio > (0.25 * fund_value):
                        cash_ratio = (0.25 * fund_value)
                    portfolio_cash[i] = cash_ratio
                    portfolio_weights[i] = cash_ratio / fund_value
                    portfolio_number_of_stocks[i] = cash_ratio / current_month[i]
                    cash -= cash_ratio

        # if some fund is left ,buy the rest of stocks starting from the most attractive stock till 0.25
        # print(portfolio_weights)
        # print("Cash" + str(cash))
        while (cash > c_max):
            # print("true")
            for i in list_stocks:
                if portfolio_weights[i] < 0.25 and portfolio_weights[i] > 0:
                    missing_cash = fund_value * (0.25 - portfolio_weights[i])
                    if (missing_cash > cash):
                        missing_cash = cash
                    portfolio_cash[i] += missing_cash
                    portfolio_weights[i] += missing_cash / fund_value
                    portfolio_number_of_stocks[i] += missing_cash / current_month[i]
                    cash -= missing_cash
                    # print("FUND VALUE " + str(fund_value))
                    # print( "===========================================================================================================")
    # calculate Avg Risk and Avg Return of the current model
    # print(Value)
    # print(len(Value))
    # print(Value)
    # print(Ind_Value)
    # print(len(Ind_Value))
    for i in range(1, len(date_60)):
        Return.append((Value[i] - Value[i - 1]) / Value[i - 1])
        index_return.append((Ind_Value[i] - Ind_Value[i - 1]) / Ind_Value[i - 1])
    numerator = 0
    denominator = len(date_60)
    for i in range(len(Return)):
        if (Return[i] > index_return[i]):
            numerator += 1

    probability = numerator / denominator
    # print(probability)
    # Return_array = np.array(Return)
    # Avg_Return = Return_array.mean() * 12
    # Avg_Risk = Return_array.std() * 3.46
    # print(Value[40])
    return probability
