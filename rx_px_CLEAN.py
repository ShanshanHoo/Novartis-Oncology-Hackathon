# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 17:11:00 2020

@author: 31509
"""

import pandas as pd
import numpy as np
import seaborn as sns #visualisation
import matplotlib.pyplot as plt #visualisation

def label_brand (row):
   if row['drug_generic_name'] == 'PALBOCICLIB' or row['drug_name'] == 'IBRANCE':
      return 'IBR'
   if row['drug_generic_name'] == 'FULVESTRANT' or row['drug_name'] == 'FASLODEX':
      return 'FAS'
   if row['drug_generic_name'] == 'RIBOCICLIB' or row['drug_name'] == 'KISQALI' or row['drug_name'] == 'KISQALI FEMARA' or row['drug_generic_name'] == 'RIBOCICLIB SUCCINATE-LETROZOLE':
      return 'KIS'
   if row['drug_generic_name'] == 'EVEROLIMUS' or row['drug_name'] == 'AFINITOR':
      return 'AFI'
   if row['drug_generic_name'] == 'LETROZOLE' or row['drug_name'] == 'FEMARA':
      return 'LET'
   if row['drug_generic_name'] == 'ABEMACICLIB' or row['drug_name'] == 'VERZENIO':
      return 'VER'
   if row['drug_generic_name'] == 'CHEMO' or row['drug_name'] == 'CHEMO':
      return 'CHEMO'
   if row['drug_generic_name'] == 'CAPECITABINE' or row['drug_name'] == 'XELODA':
      return 'XEL'
   if row['drug_name'] == 'TAMOXIFEN CITRATE':
      return 'TAM'
   if row['drug_generic_name'] == 'ANASTROZOLE' or row['drug_generic_name'] == 'EXEMESTANE' or row['drug_name'] == 'ANASTROZOLE' or row['drug_name'] == 'ARIMIDEX' or row['drug_name'] == 'EXEMESTANE' or row['drug_name'] == 'AROMASIN' or row['drug_name'] == 'NOLVADEX' or row['drug_name'] == 'SOLTAMOX':
      return 'AI'
   return 'OTHERS'

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
                 ,'REFILL_CODE','DSPNSD_QTY','DAYS_SUPPLY'],inplace=True)                                                             
rx.drop_duplicates(subset=['PATIENT_ID','DIAGNOSIS_CODE','DIAG_VERS_TYP_ID','drug_id'],keep='first',inplace=True)
## for DIAG_VERS_TYP_ID, fill nan with -1
rx['DIAG_VERS_TYP_ID'].fillna('-1',inplace=True)
## lable drug name
rx=pd.merge(rx,dg_rf,how='left',on='drug_id',validate="m:1")
rx['brand'] = rx.apply (lambda row: label_brand(row), axis=1)




## turn DIAGNOSIS_CODE & REFILL_CODE to dummy variables
rx_dummy=pd.get_dummies(rx, columns=['DIAGNOSIS_CODE','DIAG_VERS_TYP_ID','drug_generic_name'])
rx_dummy.isna().sum()
rx_dummy.to_csv('rx_clean.csv')






# clean PX----------------------------------------------------------------------------------------------
## drop
px.drop(columns=['CLAIM_ID','CLAIM_LINE_ITEM','PRC1_MOD_CD','PRC1_MOD_DESC','PROVIDER_BILLING_ID','PROVIDER_FACILITY_ID','PROVIDER_REFERRING_ID','PROVIDER_RENDERING_ID',
                 'SVC_CRGD_AMT','PLACE_OF_SERVICE','PAYER_PLAN_ID','PAY_TYPE','PRODUCT','DIAG_CD_POSN_NBR','DIAG_DESC','WEEK_END_FRI','RESTATE_FLAG',
                 'FLEXIBLE_FLD_1_CHAR','FLEXIBLE_FLD_2_CHAR','CLAIM_TYP_CD','NDC'],inplace=True)
px.drop_duplicates(subset=['PATIENT_ID','drug_id','DIAG_VERS_TYP_ID','DIAGNOSIS_CODE','PRC_VERS_TYP_ID'],keep='first',inplace=True)
## for PRC_VERS_TYP_ID, fill nan with -1
px['PRC_VERS_TYP_ID'].fillna('-1',inplace=True)
## lable drug name
px=pd.merge(px,dg_rf,how='left',on='drug_id',validate="m:1")
px['brand'] = px.apply (lambda row: label_brand(row), axis=1)
## for UNIT_OF_SVC_AMT, fill nan with 0
px['UNIT_OF_SVC_AMT'].fillna(0,inplace=True)







## dummy CLAIM_LINE_ITEM, PRC_VERS_TYP_ID, NDC, DIAGNOSIS_CODE
px_dummy=pd.get_dummies(px, columns=['PRC_VERS_TYP_ID','DIAGNOSIS_CODE','DIAG_VERS_TYP_ID'])
px_dummy.isna().sum()
px_dummy.to_csv('px_clean.csv')