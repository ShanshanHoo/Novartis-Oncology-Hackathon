#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 23:26:28 2020

@author: siqisun
"""
#Combine RX and PX claims data, rename NDC in RX and Procedure_code in PX as drug_id, file namae is "rx_px_combine.csv"
import os
import pandas as pd
os.chdir("/Users/siqisun/Documents/graduate1/novartis hackthon/")

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

rx_fil = rx.loc[:, ["PATIENT_ID", "CLAIM_ID", "MONTH_ID", "SERVICE_DATE", "NDC", "DIAGNOSIS_CODE"]]
px_fil = px.loc[:, ["PATIENT_ID", "CLAIM_ID",  "MONTH_ID", "SERVICE_DATE", "PROCEDURE_CODE", "DIAGNOSIS_CODE"]]

rx_fil = rx_fil.rename(columns={"NDC":"drug_id"})
rx_fil = rx_fil.fillna("0")

px_fil = px_fil.rename(columns={"PROCEDURE_CODE":"drug_id",})
px_fil = px_fil.fillna("0")
# rx_fil.shape (317323, 5)
# px_fil.shape (9297565, 5)
px_fil_nodup = px_fil.drop_duplicates()
#px_fil_nodup.shape (8613515, 5), indicates duplicates rows, this px dataframe will be further used for merge with rx
rx_fil_nodup = rx_fil.drop_duplicates()
#rx_fil_nodup.shape (317322, 5), indicates all the records are unique

merged = rx_fil_nodup.append(px_fil_nodup, ignore_index=True)
merged = merged.fillna("0")
#merged.shape (8930838, 5)

''' all the following are QC
len(rx_fil[rx_fil.loc[:, "RX_CLAIM_ID"] != "0"]) #317323, comapred to rx_fil, indicates all rx are linked with the claim id
len(rx_fil.loc[:, "RX_CLAIM_ID"].unique())#317322, inidates all rx claim ids are unique 

len(px_fil[px_fil.loc[:, "PX_CLAIM_ID"] != "0"]) #9297565 comapred to px_fil, indicates all px are linked with the claim id
len(px_fil.loc[:, "PX_CLAIM_ID"].unique())#1734748, inidates some px_claim ids are correlated with multiple records
len(px['PATIENT_ID'].unique()) #20000, indcates 1 patient have mutliple px claims

all_claims = rx_fil.loc[:, "RX_CLAIM_ID"]
all_claims = all_claims.append(px_fil_nodup.loc[:, "PX_CLAIM_ID"]) 
len(all_claims) #8930838
len(all_claims.unique()) #2052070, indicate rx_claim_ids overlap with PX_CLAIM_ID
'''

merged = merged.sort_values(by="PATIENT_ID", ascending=False) 
merged_nodup = merged.drop_duplicates()
#merged_nodup.shape (8930837, 5), indicates rx records dont fully overlap with px records
merged.to_csv("rx_px_combine_2l.csv", index = False)
