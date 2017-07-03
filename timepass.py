import pandas as pd
import os
import pickle
import numpy as np
# with open('df_dict.pkl', 'rb') as f:
#     df_dict = pickle.load(f)
#
# df1 = df_dict['Britania'].copy(deep=True)
# with open('iter.pkl', 'rb') as f:
#     iter_pk = pickle.load(f)
#
with open('df_dict.pkl', 'rb') as f:
    df_dict= pickle.load(f)
for i in df_dict.keys():
    print(df_dict[i])
# date_index=iter_pk*12 +12+month
# date = df1.index.values[date_index]
# print(iter_pk)
# print(month)
# print(date)

# df_dict=dict()
# for files in os.listdir("FMCG"):
#     df=pd.read_excel("FMCG//" + files + "//" + files + "_full.xlsx",sheetname=0)
#     df.set_index('Date',inplace=True)
#     df = df[['Open','Close']]
#     df_dict[files]=df
#
# for files in os.listdir("FMCG"):
#     print("==============="+files+"====================")
# #     print(df_dict[files].head())
# with open('df_dict_oc.pkl', 'rb') as f:
#     df_d=pickle.load(f)
# for files in os.listdir("FMCG"):
#     print("===============" + files + "====================")
#     print(df_d[files].head())
# # ret=2.4
# # print((ret)**(1/12))
# prod=1
# Value=[ 0.02277039, -0.08773548 , 0.01817552 , 0.09218806,  0.10919835 , 0.01182195,-0.01965659 ,-0.04064096,  0.02530307,  0.05211638 , 0.03164741 , 0.21227312]
# Return_array=np.array(Value)
# RETURN=[]
# # Return_array=Return_array/100
#
# for ret in Return_array:
#         RETURN.append(1+ret)
# print(RETURN)
# for RET in RETURN:
#     prod=prod*RET
#
# Avg_Return = prod-1
# print(Avg_Return)
# Return0.00427971939223
# Risk0.00255310282719
# iter_pk=5
# with open("iter.pkl","wb") as f:
#     pickle.dump(iter_pk,f)
