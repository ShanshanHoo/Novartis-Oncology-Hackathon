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

# clean RX
## drop FLEXIBLE_FLD_1_CHAR, FLEXIBLE_FLD_2_CHAR, PAYER_PLAN_ID, CLAIM_ID, RESTATE_FLAG
rx.drop(columns=['FLEXIBLE_FLD_1_CHAR','FLEXIBLE_FLD_2_CHAR','PAYER_PLAN_ID','CLAIM_ID','PROVIDER_ID','RESTATE_FLAG'],inplace=True)
## check unique value of each columns
print('unmber of unique value: ', '\n', 'PATIENT_ID ', len(rx['PATIENT_ID'].unique()),'\n',
      'drug_id ', len(rx['drug_id'].unique()),'\n',
      'DIAGNOSIS_CODE ', len(rx['DIAGNOSIS_CODE'].unique()),'\n',
      'DIAG_VERS_TYP_ID ', len(rx['DIAG_VERS_TYP_ID'].unique()),'\n',
      'REFILL_CODE ', len(rx['REFILL_CODE'].unique()),'\n',
      'DSPNSD_QTY ', len(rx['DSPNSD_QTY'].unique()),'\n',
      'DAYS_SUPPLY ', len(rx['DAYS_SUPPLY'].unique()),'\n',
      'SERVICE_DATE ', len(rx['SERVICE_DATE'].unique()),'\n',
     'MONTH_ID ', len(rx['MONTH_ID'].unique()),'\n')
## for DIAG_VERS_TYP_ID, fill nan with -1
rx['DIAG_VERS_TYP_ID'].isnull().any()
rx['DIAG_VERS_TYP_ID'].unique()
rx['DIAG_VERS_TYP_ID'].fillna('-1',inplace=True)
rx['DIAG_VERS_TYP_ID'].unique()
## turn DIAGNOSIS_CODE & REFILL_CODE to dummy variables
rx_dummy=pd.get_dummies(rx, columns=['DIAGNOSIS_CODE','REFILL_CODE'])
rx_dummy.isna().sum()
rx_dummy.to_csv('rx_clean.csv')


# clean PX
## drop PRC1_MOD_DESC, PROVIDER_BILLING_ID, PROVIDER_FACILITY_ID, PROVIDER_REFERRING_ID, PROVIDER_RENDERING_ID, SVC_CRGD_AMT, PLACE_OF_SERVICE, 
## PAYER_PLAN_ID, PAY_TYPE, PRODUCT, DIAG_DESC, WEEK_END_FRI, RESTATE_FLAG, FLEXIBLE_FLD_1_CHAR, FLEXIBLE_FLD_2_CHAR
px.drop(columns=['CLAIM_ID','PRC1_MOD_DESC','PROVIDER_BILLING_ID','PROVIDER_FACILITY_ID','PROVIDER_REFERRING_ID','PROVIDER_RENDERING_ID',
                 'SVC_CRGD_AMT','PLACE_OF_SERVICE','PAYER_PLAN_ID','PAY_TYPE','PRODUCT','DIAG_DESC','WEEK_END_FRI','RESTATE_FLAG',
                 'FLEXIBLE_FLD_1_CHAR','FLEXIBLE_FLD_2_CHAR','CLAIM_TYP_CD'],inplace=True)
## check unique value of each columns
print('unmber of unique value: ', '\n', 'PATIENT_ID ', len(px['PATIENT_ID'].unique()),'\n',
      'CLAIM_LINE_ITEM ', len(px['CLAIM_LINE_ITEM'].unique()),'\n',
      'drug_id ', len(px['drug_id'].unique()),'\n',
      'PRC1_MOD_CD ', len(px['PRC1_MOD_CD'].unique()),'\n',
      'PRC_VERS_TYP_ID ', len(px['PRC_VERS_TYP_ID'].unique()),'\n',
     'SERVICE_DATE ', len(px['SERVICE_DATE'].unique()),'\n',
     'MONTH_ID ', len(px['MONTH_ID'].unique()),'\n',
     'UNIT_OF_SVC_AMT ', len(px['UNIT_OF_SVC_AMT'].unique()),'\n',
     'NDC ', len(px['NDC'].unique()),'\n',
     'DIAGNOSIS_CODE ', len(px['DIAGNOSIS_CODE'].unique()),'\n',
     'DIAG_CD_POSN_NBR ', len(px['DIAG_CD_POSN_NBR'].unique()),'\n',
     'DIAG_VERS_TYP_ID ', len(px['DIAG_VERS_TYP_ID'].unique()),'\n')
## for PRC_VERS_TYP_ID, fill nan with -1
px['PRC_VERS_TYP_ID'].isnull().any()
px['PRC_VERS_TYP_ID'].unique()
px['PRC_VERS_TYP_ID'].fillna('-1',inplace=True)
px['PRC_VERS_TYP_ID'].unique()
## for UNIT_OF_SVC_AMT, fill nan with 0
px['UNIT_OF_SVC_AMT'].fillna(0,inplace=True)
## dummy CLAIM_LINE_ITEM, PRC1_MOD_CD, PRC_VERS_TYP_ID, NDC, DIAGNOSIS_CODE
px_dummy=pd.get_dummies(px, columns=['CLAIM_LINE_ITEM','PRC1_MOD_CD','PRC_VERS_TYP_ID','NDC','DIAGNOSIS_CODE'])
px_dummy.isna().sum()
px_dummy.to_csv('px_clean.csv')

################################################# 输出的是px_dummy.csv和rx_dummy.csv

# merge PX and RX

