# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 11:44:15 2020

@author: Shanshan Hu
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
import re
from sklearn.model_selection import train_test_split
from numpy import savetxt

os.chdir("/Users/conta/Documents/Novartis")

px = pd.read_csv('PX_2l.txt', 
                   dtype={"PATIENT_ID": int,"CLAIM_ID": object,"CLAIM_LINE_ITEM": int,
                          "CLAIM_TYP_CD": object,"PROCEDURE_CODE": object,"PRC1_MOD_CD": object,"PRC1_MOD_DESC": object,
                          "PRC_VERS_TYP_ID": object,"PROVIDER_BILLING_ID": int,"PROVIDER_FACILITY_ID": int,
                          "PROVIDER_REFERRING_ID": int,"PROVIDER_RENDERING_ID": int,"SVC_CRGD_AMT": float,
                          "SERVICE_DATE": str,"MONTH_ID": int,"UNIT_OF_SVC_AMT": float,
                          "PLACE_OF_SERVICE": object,"PAYER_PLAN_ID": object,"PAY_TYPE": object,"NDC": object,
                          "PRODUCT": object,"DIAGNOSIS_CODE": object,"DIAG_CD_POSN_NBR": int,"DIAG_VERS_TYP_ID": int,
                          "DIAG_DESC": object,"WEEK_END_FRI": object,
                          "RESTATE_FLAG": object,"FLEXIBLE_FLD_1_CHAR": object,"FLEXIBLE_FLD_2_CHAR": object}, 
                   sep="|")

rx = pd.read_csv('RX_2l.txt', 
                   dtype={"PATIENT_ID": int,"CLAIM_ID": object,"NDC": object,"PROVIDER_ID": object,
                          "DIAGNOSIS_CODE": object,"DIAG_VERS_TYP_ID": object,"PAYER_PLAN_ID": object,
                          "REFILL_CODE": object,"DSPNSD_QTY": float,"DAYS_SUPPLY": int,"SERVICE_DATE": str,
                          "MONTH_ID": int,
                          "RESTATE_FLAG": object,"FLEXIBLE_FLD_1_CHAR": object,"FLEXIBLE_FLD_2_CHAR": object}, 
                   sep="|")

diag = pd.read_csv('DIAG_2l.txt', 
                   dtype={"PATIENT_ID": int,"CLAIM_ID": object,"CLAIM_TYP_CD": object,"SERVICE_DATE": str,"MONTH_ID": int,
                          "DIAGNOSIS_CODE": object,"DIAG_VERS_TYP_ID": int,"DIAG_CD_POSN_NBR": int,"PROVIDER_ID": object,
                          "RESTATE_FLAG": object,"FLEXIBLE_FLD_1_CHAR": object,"FLEXIBLE_FLD_2_CHAR": object}, 
                   sep="|")

# unique px patient ID 20000, diag patient ID 20000, rx patient ID 19708
id_train, id_test = train_test_split(px['PATIENT_ID'].unique(), test_size=0.25, random_state=42)

savetxt('id_train_2l.csv', id_train, delimiter=',')
savetxt('id_test_2l.csv', id_test, delimiter=',')

#df1 = pd.DataFrame(rx['PATIENT_ID'].unique())
#df2 = pd.DataFrame(diag['PATIENT_ID'].unique())
#df3 = pd.DataFrame(px['PATIENT_ID'].unique())
#intersected_df1 = pd.merge(df1, df2, how='inner')
#intersected_df2 = pd.merge(df3, df2, how='inner')
#intersected_df3 = pd.merge(df3, df1, how='inner')
#len(intersected_df1) # 19708
#len(intersected_df2) # 20000
#len(intersected_df3) # 19708