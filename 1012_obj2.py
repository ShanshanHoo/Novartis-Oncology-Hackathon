import numpy as np
from sklearn import random_projection
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report as cr
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
import os
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
import re
import datetime
px_l = pd.read_csv('PX_2l.txt',
                 dtype={"PATIENT_ID": int,"CLAIM_ID": object,"CLAIM_LINE_ITEM": int,
                          "CLAIM_TYP_CD": object,"PROCEDURE_CODE": object,"PRC1_MOD_CD": object,"PRC1_MOD_DESC": object,
                          "PRC_VERS_TYP_ID": object,"PROVIDER_BILLING_ID": int,"PROVIDER_FACILITY_ID": int,
                          "PROVIDER_REFERRING_ID": int,"PROVIDER_RENDERING_ID": int,"SVC_CRGD_AMT": float,
                          "SERVICE_DATE": str,"MONTH_ID": int,"UNIT_OF_SVC_AMT": float,
                          "PLACE_OF_SERVICE": object,"PAYER_PLAN_ID": object,"PAY_TYPE": object,"NDC": object,
                          "PRODUCT": object,"DIAGNOSIS_CODE": object,"DIAG_CD_POSN_NBR": int,"DIAG_VERS_TYP_ID": int,
                          "DIAG_DESC": object,"WEEK_END_FRI": object,
                          "RESTATE_FLAG": object,"FLEXIBLE_FLD_1_CHAR": object,"FLEXIBLE_FLD_2_CHAR": object},sep='|',header=0)

px_l.rename(index=str, columns={"PROCEDURE_CODE": "drug_id"},inplace=True)

rx_l =pd.read_csv('RX_2l.txt',
                 dtype={"PATIENT_ID": int,"CLAIM_ID": object,"NDC": object,"PROVIDER_ID": object,
                          "DIAGNOSIS_CODE": object,"DIAG_VERS_TYP_ID": object,"PAYER_PLAN_ID": object,
                          "REFILL_CODE": object,"DSPNSD_QTY": float,"DAYS_SUPPLY": int,"SERVICE_DATE": str,
                          "MONTH_ID": int,
                          "RESTATE_FLAG": object,"FLEXIBLE_FLD_1_CHAR": object,"FLEXIBLE_FLD_2_CHAR": object}, sep='|',header=0)

rx_l.rename(index=str, columns={'NDC':'drug_id'},inplace=True)

px_l.sort_values(by=['PATIENT_ID'],ascending=(False),inplace=True)
rx_l.sort_values(by=['PATIENT_ID'],ascending=(False),inplace=True)

rx_l.drop(columns=['CLAIM_ID','PAYER_PLAN_ID', 'REFILL_CODE', 'DSPNSD_QTY','RESTATE_FLAG','FLEXIBLE_FLD_1_CHAR', 'FLEXIBLE_FLD_2_CHAR'],inplace=True)

px_l.drop(columns=['CLAIM_ID', 'CLAIM_LINE_ITEM','PRC1_MOD_CD', 'PRC1_MOD_DESC','PROVIDER_BILLING_ID', 'PROVIDER_FACILITY_ID',
                   'PROVIDER_REFERRING_ID','PROVIDER_RENDERING_ID', 'SVC_CRGD_AMT','PAYER_PLAN_ID', 'PAY_TYPE','PRODUCT','DIAG_CD_POSN_NBR',
                   'DIAG_DESC', 'WEEK_END_FRI', 'RESTATE_FLAG','FLEXIBLE_FLD_1_CHAR', 'FLEXIBLE_FLD_2_CHAR'],inplace=True)

dg_rf = pd.read_csv('drug_ref.csv', dtype={'drug_id':str,'drug_name':str,'drug_generic_name':str},header=0)
dg_rf = dg_rf.rename(columns={"drug_id ":"drug_id"})
dg_rf = dg_rf[dg_rf.columns[0:3]] 


rx_l=pd.merge(rx_l,dg_rf,how='left',on='drug_id',validate="m:1")
rx_l.loc[(rx_l['drug_generic_name']=='PALBOCICLIB') | (rx_l['drug_name']=='IBRANCE'),'brand']='IBR'
rx_l.loc[(rx_l['drug_generic_name']=='FULVESTRANT') | (rx_l['drug_name']=='FASLODEX'),'brand']='FAS'
rx_l.loc[(rx_l['drug_generic_name']=='RIBOCICLIB') | (rx_l['drug_name']=='KISQALI') | (rx_l['drug_name']=='KISQALI FEMARA') | (rx_l['drug_generic_name']=='RIBOCICLIB SUCCINATE-LETROZOLE'),'brand']='KIS'
rx_l.loc[(rx_l['drug_generic_name']=='EVEROLIMUS') | (rx_l['drug_name']=='AFINITOR'),'brand']='AFI'
rx_l.loc[(rx_l['drug_generic_name']=='LETROZOLE') | (rx_l['drug_name']=='FEMARA'),'brand']='LET'
rx_l.loc[(rx_l['drug_generic_name']=='ABEMACICLIB') | (rx_l['drug_name']=='VERZENIO'),'brand']='VER'
rx_l.loc[(rx_l['drug_generic_name']=='CHEMO') | (rx_l['drug_name']=='CHEMO'),'brand']='CHEMO'
rx_l.loc[(rx_l['drug_generic_name']=='CAPECITABINE') | (rx_l['drug_name']=='XELODA'),'brand']='XEL'
rx_l.loc[(rx_l['drug_name']=='TAMOXIFEN CITRATE'),'brand']='TAM'
rx_l.loc[(rx_l['drug_generic_name']=='ANASTROZOLE') | (rx_l['drug_generic_name']=='EXEMESTANE') | (rx_l['drug_name']=='ANASTROZOLE') | 
         (rx_l['drug_name']=='ARIMIDEX') | (rx_l['drug_name']=='EXEMESTANE') | 
        (rx_l['drug_name']=='AROMASIN')|(rx_l['drug_name']=='NOLVADEX')|(rx_l['drug_name']=='SOLTAMOX'),'brand']='AI'
rx_l.drop(columns=['drug_id','drug_name','drug_generic_name'],inplace=True)

rx_l.drop_duplicates(keep='first',inplace=True)


px_l=pd.merge(px_l,dg_rf,how='left',on='drug_id',validate="m:1")
px_l.loc[(px_l['drug_generic_name']=='PALBOCICLIB') | (px_l['drug_name']=='IBRANCE'),'brand']='IBR'
px_l.loc[(px_l['drug_generic_name']=='FULVESTRANT') | (px_l['drug_name']=='FASLODEX'),'brand']='FAS'
px_l.loc[(px_l['drug_generic_name']=='RIBOCICLIB') | (px_l['drug_name']=='KISQALI') | (px_l['drug_name']=='KISQALI FEMARA') | (px_l['drug_generic_name']=='RIBOCICLIB SUCCINATE-LETROZOLE'),'brand']='KIS'
px_l.loc[(px_l['drug_generic_name']=='EVEROLIMUS') | (px_l['drug_name']=='AFINITOR'),'brand']='AFI'
px_l.loc[(px_l['drug_generic_name']=='LETROZOLE') | (px_l['drug_name']=='FEMARA'),'brand']='LET'
px_l.loc[(px_l['drug_generic_name']=='ABEMACICLIB') | (px_l['drug_name']=='VERZENIO'),'brand']='VER'
px_l.loc[(px_l['drug_generic_name']=='CHEMO') | (px_l['drug_name']=='CHEMO'),'brand']='CHEMO'
px_l.loc[(px_l['drug_generic_name']=='CAPECITABINE') | (px_l['drug_name']=='XELODA'),'brand']='XEL'
px_l.loc[(px_l['drug_name']=='TAMOXIFEN CITRATE'),'brand']='TAM'
px_l.loc[(px_l['drug_generic_name']=='ANASTROZOLE') | (px_l['drug_generic_name']=='EXEMESTANE') | (px_l['drug_name']=='ANASTROZOLE') | 
         (px_l['drug_name']=='ARIMIDEX') | (px_l['drug_name']=='EXEMESTANE') | 
        (px_l['drug_name']=='AROMASIN')|(px_l['drug_name']=='NOLVADEX')|(px_l['drug_name']=='SOLTAMOX'),'brand']='AI'
px_l.drop(columns=['drug_id','drug_name','drug_generic_name'],inplace=True)

px_l.drop_duplicates(keep='first',inplace=True)



pxrxl = pd.concat([px_l,rx_l],ignore_index=True)
pxrxl.drop(columns=['PLACE_OF_SERVICE','PROVIDER_ID','CLAIM_TYP_CD','MONTH_ID','DAYS_SUPPLY'],inplace=True)
#pxrxl.drop(columns=['PLACE_OF_SERVICE','PROVIDER_ID','CLAIM_TYP_CD','MONTH_ID','DAYS_SUPPLY','NDC','DIAGNOSIS_CODE'],inplace=True)


pxrxl = pxrxl.sort_values(by=['PATIENT_ID','SERVICE_DATE'],ascending=(False,True))
pxrxl.reset_index(drop=True,inplace=True)
pxrxl = pxrxl.drop_duplicates(subset=['PATIENT_ID','NDC', 'DIAGNOSIS_CODE', 'DIAG_VERS_TYP_ID', 'brand','PRC_VERS_TYP_ID','UNIT_OF_SVC_AMT'])


pxrxl['SERVICE_DATE'] = pd.to_datetime(pxrxl['SERVICE_DATE'])
pxrxl['SERVICE_DATE'] = pxrxl['SERVICE_DATE'].dt.date
pxrxl = pxrxl.sort_values(by=['PATIENT_ID','SERVICE_DATE'],ascending=(False,True))
pxrxl.reset_index(drop=True,inplace=True)

day_diff = pd.Series()

plist = list(pxrxl['PATIENT_ID'].unique())
for i in range(len(plist)):
    start = pxrxl[pxrxl['PATIENT_ID']==plist[i]]['SERVICE_DATE'].iloc[0]
    diff = pxrxl[pxrxl['PATIENT_ID']==plist[i]]['SERVICE_DATE']-start
    day_diff=pd.concat([day_diff,diff])
    
pxrxl['day_diff']=day_diff.dt.days

pxrxl['day_diff']=pd.to_numeric(pxrxl['day_diff'])

pxrxl['y']=0
pxrxl.loc[pxrxl['day_diff']>=30, 'y'] = 1
print('# of 1 in data: ',pxrxl[pxrxl['y']==1].shape[0])
print('# of 1 in patient: ',len(pxrxl[pxrxl['y']==1]['PATIENT_ID'].unique()))

print('# of 0 in data: ',pxrxl[pxrxl['y']==0].shape[0])
print('# of 0 in patient: ',len(pxrxl[pxrxl['y']==0]['PATIENT_ID'].unique()))


#################### 要怎么处理用来跑模型的数据 请从这里开始 #############################

#pxrxl_1 = pxrxl[pxrxl['y']==1].drop_duplicates(subset=['PATIENT_ID'])
#pxrxl_try = pd.concat([pxrxl_1,pxrxl[pxrxl['y']==0]])
#pxrxl_try = pxrxl_try.sort_values(by=['PATIENT_ID','SERVICE_DATE'],ascending=(False,True))
#pxrxl_try['UNIT_OF_SVC_AMT'].fillna(0,inplace=True)
#pxrxl_try['day_diff']=(pxrxl_try['day_diff']-pxrxl_try['day_diff'].mean())/pxrxl_try['day_diff'].std()
#pxrxl_try['UNIT_OF_SVC_AMT']=(pxrxl_try['UNIT_OF_SVC_AMT']-pxrxl_try['UNIT_OF_SVC_AMT'].mean())/pxrxl_try['UNIT_OF_SVC_AMT'].std()

#########################################
pxrxl.to_csv('pxrxl1012.csv')
#########################################

result = pd.DataFrame(index=['XGBoo','RF'],columns=['tn','fp','fn','tp'])

pxrxl = pd.get_dummies(pxrxl,columns=['DIAGNOSIS_CODE','DIAG_VERS_TYP_ID','brand','PRC_VERS_TYP_ID','NDC'])

#ptlist = pxrxl['PATIENT_ID'].unique()
#train, test = train_test_split( ptlist, test_size=0.25, random_state=42)
patient_1 = list(pxrxl[pxrxl['y']==1]['PATIENT_ID'])
patient_0 = list(pxrxl[pxrxl['y']==0]['PATIENT_ID'])
train_1, test_1 = train_test_split( patient_1, test_size=0.25, random_state=42)
train_0, test_0 = train_test_split( patient_0, test_size=0.25, random_state=42)

boot=resample(train_0, replace=True, n_samples=300000)

train = train_1+train_0+boot
test = test_1+test_0
#ptlist = pxrxl['PATIENT_ID'].unique()
#train, test = train_test_split( ptlist, test_size=0.25, random_state=42)
#print('# of training: ',train.shape[0],'\n','# of testing: ',test.shape[0])

training = pxrxl.loc[pxrxl['PATIENT_ID'].isin(list(train))]
print('# of 1 in train: ',len(training[training['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in train: ',len(training[training['y']==1]['PATIENT_ID'].unique()))
y_train = training['y']
X_train = training.drop(columns=['y','PATIENT_ID','SERVICE_DATE','day_diff'])

testing = pxrxl.loc[pxrxl['PATIENT_ID'].isin(list(test))]
print('# of 1 in test: ',len(testing[testing['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in test: ',len(testing[testing['y']==1]['PATIENT_ID'].unique()))

testing.shape
y_test = testing['y']
X_test = testing.drop(columns=['y','PATIENT_ID','SERVICE_DATE','day_diff'])

########################### XGBoosting #############
xgb = XGBClassifier()
xgb.fit(X_train,y_train)
y_pred = xgb.predict(X_test)

tn_1, fp_1, fn_1, tp_1 = confusion_matrix(y_test, y_pred).ravel()
result.iloc[0,0] = tn_1
result.iloc[0,1] = fp_1
result.iloc[0,2] = fn_1
result.iloc[0,3] = tp_1

result.to_csv('result_obj2.csv')
print(result)

########################## Random Forest #############
#clf = RandomForestClassifier()
#clf.fit(X_train,y_train)
#y_pred = clf.predict(X_test)
#tn_2, fp_2, fn_2, tp_2 = confusion_matrix(y_test, y_pred).ravel()
#result.iloc[1,0] = tn_2
#result.iloc[1,1] = fp_2
#result.iloc[1,2] = fn_2
#result.iloc[1,3] = tp_2
#
#result.to_csv('result_obj1.csv')
#print(result)
