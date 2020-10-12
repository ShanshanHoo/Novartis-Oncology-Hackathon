# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 20:41:13 2020

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

os.chdir("/Users/conta/Documents/Novartis")

## merge rx_px_combine with drug reference
prx = pd.read_csv('rx_px_combine_2l.csv', header=0)

dg_rf = pd.read_csv('Drug Reference1.csv', dtype={"drug_id ": str,"drug_name": str,"drug_generic_name": str},header=0)
dg_rf = dg_rf[dg_rf.columns[0:3]] 
dg_rf = dg_rf.rename(columns={"drug_id ":"drug_id"})
dg_rf.head()
dg=pd.merge(prx,dg_rf,how='left',on='drug_id',validate="m:1")

# check intersection, check merge accuracy
len(dg['drug_id'].unique()) # 7806
len(dg_rf['drug_id'].unique()) # 532725
len(dg_rf) # 532725
len(prx['drug_id'].unique()) # 7806
len(prx) # 8930837
df2 = pd.DataFrame(dg_rf['drug_id'].unique())
df3 = pd.DataFrame(prx['drug_id'].unique())
intersected_df = pd.merge(df3, df2, how='inner')
len(intersected_df) # 21

df2 = pd.DataFrame(dg_rf['drug_id'])
df3 = pd.DataFrame(prx['drug_id'])
intersected_df = pd.merge(df3, df2, how='inner')
len(intersected_df) # 429451
len(intersected_df['drug_id'].unique()) # 21

dg.to_csv("drug_pxrx_2l.csv", index = False)

#px = pd.read_csv('PX.txt', 
#                   dtype={"PATIENT_ID": int,"CLAIM_ID": object,"CLAIM_LINE_ITEM": int,
#                          "CLAIM_TYP_CD": object,"PROCEDURE_CODE": object,"PRC1_MOD_CD": object,"PRC1_MOD_DESC": object,
#                          "PRC_VERS_TYP_ID": object,"PROVIDER_BILLING_ID": int,"PROVIDER_FACILITY_ID": int,
#                          "PROVIDER_REFERRING_ID": int,"PROVIDER_RENDERING_ID": int,"SVC_CRGD_AMT": float,
#                          "SERVICE_DATE": str,"MONTH_ID": int,"UNIT_OF_SVC_AMT": float,
#                          "PLACE_OF_SERVICE": object,"PAYER_PLAN_ID": object,"PAY_TYPE": object,"NDC": object,
#                          "PRODUCT": object,"DIAGNOSIS_CODE": object,"DIAG_CD_POSN_NBR": int,"DIAG_VERS_TYP_ID": int,
#                          "DIAG_DESC": object,"WEEK_END_FRI": object,
#                          "RESTATE_FLAG": object,"FLEXIBLE_FLD_1_CHAR": object,"FLEXIBLE_FLD_2_CHAR": object}, 
#                   sep="|")
#
#dg_rf = pd.read_csv('Drug Reference.csv',header=0)
#dg_rf = dg_rf[dg_rf.columns[0:3]] 
#dg_rf.head()
#
#px.rename(columns={'PROCEDURE_CODE':'drug_id'}, inplace=True)
#px.columns
#dg=pd.merge(px,dg_rf,how='outer',on='drug_id',validate="m:1")
#
## check intersect, check merge accuracy
#df2 = pd.DataFrame(dg_rf['drug_id'].unique())
#df3 = pd.DataFrame(px['drug_id'].unique())
#intersected_df = pd.merge(df3, df2, how='inner')
#len(intersected_df) # 20
#
#df2 = pd.DataFrame(dg_rf['drug_id'])
#df3 = pd.DataFrame(px['drug_id'])
#intersected_df = pd.merge(df3, df2, how='inner')
#len(intersected_df) # 475688
#len(px) # 9297565
#len(dg_rf) # 532725
#len(intersected_df['drug_id'].unique()) # 20




