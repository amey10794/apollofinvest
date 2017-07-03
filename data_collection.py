import os
import pandas as pd
import xlsxwriter


#
# for file in os.listdir('FMCG'):
#     workbook = xlsxwriter.Workbook('FMCG//'+file+'//'+file+'_BV.xlsx')
#
# for file in os.listdir("FMCG"):
#     print("=============="+file+"==================")
#     df_price = pd.read_excel("FMCG//"+file+"//"+file+"_basic.xlsx", sheetname=0)
#     df_price.set_index('Date',inplace=True)
#     print(df_price.head())
#     df_EPS=pd.read_excel("FMCG//"+file+"//"+file+"_EPS.xlsx", sheetname=0)
#     df_EPS.set_index('Date',inplace=True)
#     # print(df_EPS.head())
#     # print(df_price.head())
#     quarters=list()
#     for date in df_EPS.index:
#         quarters.append(date)
#     # print(quarters)
#
#
#     for date in df_price.index:
#             trailing_list=[]
#             for quarter in quarters:
#                 if (date - quarter == 1 or date - quarter == 2 or date - quarter == 3 or date - quarter == 89 or date - quarter == 90 or date - quarter == 91):
#                     ind = quarters.index(quarter)
#                     trailing_list.append(quarters[ind])
#                     trailing_list.append(quarters[ind + 1])
#                     trailing_list.append(quarters[ind + 2])
#                     trailing_list.append(quarters[ind + 3])
#             EPS=0
#             for elem in trailing_list:
#                 EPS = EPS+ df_EPS.get_value(elem,df_EPS.columns[0])
#             price = df_price.get_value(date, df_price.columns[0])
#             PE=price/EPS
#             df_price.ix[date, 'P/E'] = PE
#
#     writer = pd.ExcelWriter("FMCG//"+file+"//"+file+'_data.xlsx')
#     df_price.to_excel(writer,'Sheet1')
#     writer.save()
#     print(df_price.head())



#
# for file in os.listdir("FMCG"):
#     print("==============" + file + "==================")
#     df_price = pd.read_excel("FMCG//"+file+"//"+file+"_data.xlsx", sheetname=0)
#     df_price.set_index('Date',inplace=True)
#     # print(df_price.head())
#     df_BV=pd.read_excel("FMCG//"+file+"//"+file+"_BV.xlsx", sheetname=0)
#     df_BV.set_index('Year',inplace=True)
#     # print(df_BV.head())
#     # print(df_price.head())
#     for date in df_price.index:
#         year=int(str(date)[0:4])
#         price = df_price.get_value(date, df_price.columns[0])
#         BV=df_BV.get_value(year,df_BV.columns[0])
#         df_price.ix[date,'PB']=(price/BV)
#
#     writer = pd.ExcelWriter("FMCG//"+file+"//"+file+'_data.xlsx')
#     df_price.to_excel(writer,'Sheet1')
#     writer.save()
#     print(df_price.head())


#
#
# for file in os.listdir("FMCG"):
#     print("==============" + file + "==================")
#     df_price = pd.read_excel("FMCG//"+file+"//"+file+"_data.xlsx", sheetname=0)
#     df_price.set_index('Date',inplace=True)
#     df_ratio=pd.read_excel("FMCG//"+file+"//"+file+"_ratios.xlsx", sheetname=0)
#     df_ratio.set_index(df_ratio.columns[0],inplace=True)
#     print(df_ratio.head())
#     for year in df_ratio.index:
#         for date in df_price.index:
#             if (str(date)[2:4] == str(year).strip()):
#                 df_price.ix[date, 'ProfitMargin'] = df_ratio.get_value(year, df_ratio.columns[0])
#                 df_price.ix[date, 'ROA'] = df_ratio.get_value(year, df_ratio.columns[1])
#                 df_price.ix[date, 'DebtEquity'] = df_ratio.get_value(year, df_ratio.columns[2])
#                 df_price.ix[date, 'CurrentRatio'] = df_ratio.get_value(year, df_ratio.columns[3])
#                 df_price.ix[date, 'InventoryTurnover'] = df_ratio.get_value(year, df_ratio.columns[4])
#                 df_price.ix[date, 'DividendPayout'] = df_ratio.get_value(year, df_ratio.columns[5])
#
#
#             else:
#                 pass
#
#     writer = pd.ExcelWriter("FMCG//"+file+"//"+file+'_data.xlsx')
#     df_price.to_excel(writer,'Sheet1')
#     writer.save()
#     print(df_price.head())
#
#
#
#
#

#
# for files in os.listdir("FMCG"):
#     df_price = pd.read_excel("FMCG//"+files+"//"+files+"_data.xlsx", sheetname=0)
#     df_price.set_index('Date',inplace=True)
#     df_ratio=pd.read_excel("FMCG//"+files+"//"+files+"_ratios.xlsx", sheetname=0)
#     df_ratio.set_index(df_ratio.columns[0],inplace=True)
#     for year in df_ratio.index:
#         for date in df_price.index:
#                 if (str(date)[:4].strip() == str(year).strip()):
#                     df_price.ix[date, 'ProfitMargin'] = df_ratio.get_value(year, df_ratio.columns[0])
#                     df_price.ix[date, 'ROA'] = df_ratio.get_value(year, df_ratio.columns[1])
#                     df_price.ix[date, 'DebtEquity'] = df_ratio.get_value(year, df_ratio.columns[2])
#                     df_price.ix[date, 'CurrentRatio'] = df_ratio.get_value(year, df_ratio.columns[3])
#                     df_price.ix[date, 'InventoryTurnover'] = df_ratio.get_value(year, df_ratio.columns[4])
#                     df_price.ix[date, 'DividendPayout'] = df_ratio.get_value(year, df_ratio.columns[5])
#
#
#                 else:
#                     pass
#
#     writer = pd.ExcelWriter("FMCG//" + files + "//" + files + '_full.xlsx')
#     df_price.to_excel(writer,'Sheet1')
#     writer.save()
#     print(df_price.head())
#
# for files in os.listdir("FMCG"):
#     print("======================="+files+"=================================")
#     df_price = pd.read_excel("FMCG//" + files + "//" + files + "_full.xlsx", sheetname=0)
#     df_price.set_index('Date',inplace=True)
#     df_funda = pd.read_excel("funda.xlsx", sheetname='Crude')
#     df_funda.set_index(df_funda.columns[0],inplace=True)
#     df_price=df_price.join(df_funda)
#     writer = pd.ExcelWriter("FMCG//" + files + "//" + files + '_final.xlsx')
#     df_price.to_excel(writer,'Sheet1')
#     writer.save()
#
# for files in os.listdir("FMCG"):
#     print("=======================" + files + "=================================")
#     df_price = pd.read_excel("FMCG//" + files + "//" + files + "_final.xlsx", sheetname=0)
#     df_price.set_index('Date',inplace=True)
#     df_funda = pd.read_excel("Forex.xlsx", sheetname=0)
#     df_funda.set_index(df_funda.columns[0],inplace=True)
#     df_price=df_price.reset_index().merge(df_funda,how="left").set_index("Date")
#     print(df_price.head())
#     writer = pd.ExcelWriter("FMCG//" + files + "//" + files + '_final.xlsx')
#     df_price.to_excel(writer,'Sheet1')
#     writer.save()
for files in os.listdir("FMCG"):
    print("=======================" + files + "=================================")
    df_price = pd.read_excel("FMCG//" + files + "//" + files + "_final.xlsx", sheetname=0)
    df_price.set_index('Date', inplace=True)
    print(df_price.head())