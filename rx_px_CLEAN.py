# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 17:11:00 2020

@author: 31509
"""

import pandas as pd
import numpy as np
import seaborn as sns #visualisation
import matplotlib.pyplot as plt #visualisation


# import data, sort by ascending time 
px = pd.read_csv('E:\\Hackathon_project\\rawdata\\PX.txt',
                 dtype={"PATIENT_ID": int,"CLAIM_ID": object,"CLAIM_LINE_ITEM": int,
                          "CLAIM_TYP_CD": object,"PROCEDURE_CODE": object,"PRC1_MOD_CD": object,"PRC1_MOD_DESC": object,
                          "PRC_VERS_TYP_ID": object,"PROVIDER_BILLING_ID": int,"PROVIDER_FACILITY_ID": int,
                          "PROVIDER_REFERRING_ID": int,"PROVIDER_RENDERING_ID": int,"SVC_CRGD_AMT": float,
                          "SERVICE_DATE": str,"MONTH_ID": int,"UNIT_OF_SVC_AMT": float,
                          "PLACE_OF_SERVICE": object,"PAYER_PLAN_ID": object,"PAY_TYPE": object,"NDC": object,
                          "PRODUCT": object,"DIAGNOSIS_CODE": object,"DIAG_CD_POSN_NBR": int,"DIAG_VERS_TYP_ID": int,
                          "DIAG_DESC": object,"WEEK_END_FRI": object,
                          "RESTATE_FLAG": object,"FLEXIBLE_FLD_1_CHAR": object,"FLEXIBLE_FLD_2_CHAR": object},sep='|',header=0)

rx = pd.read_csv('E:\\Hackathon_project\\rawdata\\RX.txt',
                 dtype={"PATIENT_ID": int,"CLAIM_ID": object,"NDC": object,"PROVIDER_ID": object,
                          "DIAGNOSIS_CODE": object,"DIAG_VERS_TYP_ID": object,"PAYER_PLAN_ID": object,
                          "REFILL_CODE": object,"DSPNSD_QTY": float,"DAYS_SUPPLY": int,"SERVICE_DATE": str,
                          "MONTH_ID": int,
                          "RESTATE_FLAG": object,"FLEXIBLE_FLD_1_CHAR": object,"FLEXIBLE_FLD_2_CHAR": object}, sep='|',header=0)

dg_rf = pd.read_csv('E:\\Hackathon_project\\rawdata\\Drug.csv', dtype={'drug_id':str,'drug_name':str,'drug_generic_name':str},header=0)
dg_rf = dg_rf[dg_rf.columns[0:3]] 

# remane NDC in RX and Procedure_code in PX as drug_id
px.rename(index=str, columns={"PROCEDURE_CODE": "drug_id"},inplace=True)
rx.rename(index=str, columns={'NDC':'drug_id'},inplace=True)

px.sort_values(by=['PATIENT_ID'],ascending=(False),inplace=True)
rx.sort_values(by=['PATIENT_ID'],ascending=(False),inplace=True)



# clean RX ----------------------------------------------------------------------------------------
## drop FLEXIBLE_FLD_1_CHAR, FLEXIBLE_FLD_2_CHAR, PAYER_PLAN_ID, CLAIM_ID, RESTATE_FLAG
rx.drop(columns=['FLEXIBLE_FLD_1_CHAR','FLEXIBLE_FLD_2_CHAR','PAYER_PLAN_ID','CLAIM_ID','PROVIDER_ID','RESTATE_FLAG'
                 ,'REFILL_CODE','DSPNSD_QTY','SERVICE_DATE','DAYS_SUPPLY'],inplace=True)                                                             
## lable drug name
rx=pd.merge(rx,dg_rf,how='left',on='drug_id',validate="m:1")
rx.loc[(rx['drug_generic_name']=='PALBOCICLIB') | (rx['drug_name']=='IBRANCE'),'brand']='IBR'
rx.loc[(rx['drug_generic_name']=='FULVESTRANT') | (rx['drug_name']=='FASLODEX'),'brand']='FAS'
rx.loc[(rx['drug_generic_name']=='RIBOCICLIB') | (rx['drug_name']=='KISQALI') | (rx['drug_name']=='KISQALI FEMARA') | (rx['drug_generic_name']=='RIBOCICLIB SUCCINATE-LETROZOLE'),'brand']='KIS'
rx.loc[(rx['drug_generic_name']=='EVEROLIMUS') | (rx['drug_name']=='AFINITOR'),'brand']='AFI'
rx.loc[(rx['drug_generic_name']=='LETROZOLE') | (rx['drug_name']=='FEMARA'),'brand']='LET'
rx.loc[(rx['drug_generic_name']=='ABEMACICLIB') | (rx['drug_name']=='VERZENIO'),'brand']='VER'
rx.loc[(rx['drug_generic_name']=='CHEMO') | (rx['drug_name']=='CHEMO'),'brand']='CHEMO'
rx.loc[(rx['drug_generic_name']=='CAPECITABINE') | (rx['drug_name']=='XELODA'),'brand']='XEL'
rx.loc[(rx['drug_name']=='TAMOXIFEN CITRATE'),'brand']='TAM'
rx.loc[(rx['drug_generic_name']=='ANASTROZOLE') | (rx['drug_generic_name']=='EXEMESTANE') | (rx['drug_name']=='ANASTROZOLE') | 
         (rx['drug_name']=='ARIMIDEX') | (rx['drug_name']=='EXEMESTANE') | 
        (rx['drug_name']=='AROMASIN')|(rx['drug_name']=='NOLVADEX')|(rx['drug_name']=='SOLTAMOX'),'brand']='AI'
rx.drop(columns=['drug_id','drug_name','drug_generic_name'],inplace=True)
## drop
rx.isna().sum()
rx.drop_duplicates(subset=['PATIENT_ID','DIAGNOSIS_CODE','DIAG_VERS_TYP_ID','MONTH_ID','brand'],keep='first',inplace=True)




# clean PX----------------------------------------------------------------------------------------------
## drop
px.drop(columns=['CLAIM_ID','CLAIM_LINE_ITEM','PRC1_MOD_CD','PRC1_MOD_DESC','PROVIDER_BILLING_ID','PROVIDER_FACILITY_ID','PROVIDER_REFERRING_ID','PROVIDER_RENDERING_ID',
                 'SVC_CRGD_AMT','PLACE_OF_SERVICE','PAYER_PLAN_ID','PAY_TYPE','PRODUCT','DIAG_CD_POSN_NBR','DIAG_DESC','WEEK_END_FRI','RESTATE_FLAG',
                 'FLEXIBLE_FLD_1_CHAR','FLEXIBLE_FLD_2_CHAR','CLAIM_TYP_CD','NDC','SERVICE_DATE'],inplace=True)
## lable drug name
px=pd.merge(px,dg_rf,how='left',on='drug_id',validate="m:1")
px.loc[(px['drug_generic_name']=='PALBOCICLIB') | (px['drug_name']=='IBRANCE'),'brand']='IBR'
px.loc[(px['drug_generic_name']=='FULVESTRANT') | (px['drug_name']=='FASLODEX'),'brand']='FAS'
px.loc[(px['drug_generic_name']=='RIBOCICLIB') | (px['drug_name']=='KISQALI') | (px['drug_name']=='KISQALI FEMARA') | (px['drug_generic_name']=='RIBOCICLIB SUCCINATE-LETROZOLE'),'brand']='KIS'
px.loc[(px['drug_generic_name']=='EVEROLIMUS') | (px['drug_name']=='AFINITOR'),'brand']='AFI'
px.loc[(px['drug_generic_name']=='LETROZOLE') | (px['drug_name']=='FEMARA'),'brand']='LET'
px.loc[(px['drug_generic_name']=='ABEMACICLIB') | (px['drug_name']=='VERZENIO'),'brand']='VER'
px.loc[(px['drug_generic_name']=='CHEMO') | (px['drug_name']=='CHEMO'),'brand']='CHEMO'
px.loc[(px['drug_generic_name']=='CAPECITABINE') | (px['drug_name']=='XELODA'),'brand']='XEL'
px.loc[(px['drug_name']=='TAMOXIFEN CITRATE'),'brand']='TAM'
px.loc[(px['drug_generic_name']=='ANASTROZOLE') | (px['drug_generic_name']=='EXEMESTANE') | (px['drug_name']=='ANASTROZOLE') | 
         (px['drug_name']=='ARIMIDEX') | (px['drug_name']=='EXEMESTANE') | 
        (px['drug_name']=='AROMASIN')|(px['drug_name']=='NOLVADEX')|(px['drug_name']=='SOLTAMOX'),'brand']='AI'
px.drop(columns=['drug_id','drug_name','drug_generic_name'],inplace=True)
## for UNIT_OF_SVC_AMT, fill nan with 0
px['UNIT_OF_SVC_AMT'].fillna(0,inplace=True)
## drop
px.isna().sum()
px.drop_duplicates(subset=['PATIENT_ID','MONTH_ID','DIAG_VERS_TYP_ID','DIAGNOSIS_CODE','PRC_VERS_TYP_ID','brand'],keep='first',inplace=True)



# combine RX & PX----------------------------------------------------------------------------------------------
#pxrx = pd.merge(px, rx, how='inner', on=['PATIENT_ID','MONTH_ID'])

pxrx = pd.concat([px,rx],ignore_index=True)
pxrx.drop_duplicates(inplace=True)
pxrx.sort_values(by=['PATIENT_ID'],ascending=(False),inplace=True)
pxrx['UNIT_OF_SVC_AMT'].fillna(0,inplace=True)
pxrx.reset_index(inplace=True)


pxrx.sort_values(by=['PATIENT_ID','MONTH_ID'],ascending=(False,True),inplace=True)
pxrx2 = pxrx.drop_duplicates(subset=['PATIENT_ID'],keep='first',inplace=False)
pxrx2 = pxrx2[["PATIENT_ID",'MONTH_ID']]
pxrx3=pd.merge(pxrx,pxrx2,how='left',on="PATIENT_ID")
def month_diff(row):
    a=row["MONTH_ID_x"]//100 -row["MONTH_ID_y"]//100 #year
    b=row["MONTH_ID_x"]%100 -row["MONTH_ID_y"]%100 #month
    num = a*12 + b
    return(num)
pxrx3['MONTH_DIFF'] = pxrx3.apply(lambda x:month_diff(x), axis=1)    
pxrx3.rename(index=str, columns={"MONTH_ID_x": "MONTH_ID"},inplace=True)
pxrx3.drop(columns=['MONTH_ID_y'],inplace=True)


# 
dx_mbc= pd.read_csv("/Users/shufei/Novartis/mbc and date.csv")

dx_mbc.drop(columns=['DATE_DIFF','mBC_DIAG_DATE'],inplace=True)
# only consider mbc
diag_mbc = dx_mbc.loc[dx_mbc['mBC']== 1,] 
# consider pid and monthid in pxrx
pxrx_minus = pxrx3.drop_duplicates(subset=['PATIENT_ID','MONTH_ID'],keep='first',inplace=False)

pxrx_minus2 = pxrx_minus[['PATIENT_ID','MONTH_ID']]

mider =pd.merge(pxrx_minus2,diag_mbc,how="left",on="PATIENT_ID")
mider2 = mider.loc[mider['mBC']== 1,] 
def mbc_d (row):
    if row["MONTH_ID_x"] - row["MONTH_ID_y"] >= 0:
        part1=1
    else:
        part1=0
    return part1
#lebal mbc as y
mider2['y'] = mider2.apply(lambda x:mbc_d(x), axis=1)
mider2.rename(index=str, columns={"MONTH_ID_x": "MONTH_ID"},inplace=True)
MID = mider2[["PATIENT_ID","MONTH_ID","y"]]


#combine MID 
pdr = pd.merge(pxrx3,MID,how='left',on=['PATIENT_ID','MONTH_ID'])
pdr["y"].fillna(0,inplace=True)

pdr.to_csv("mbc_model_data.csv",index=False)
