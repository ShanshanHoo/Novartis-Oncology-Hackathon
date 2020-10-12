# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 11:16:55 2020

@author: Shanshan Hu
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
import re
import datetime

os.chdir("/Users/conta/Documents/Novartis")
## Process Dx
diag = pd.read_csv('DIAG_2l.txt', 
                   dtype={"PATIENT_ID": int,"CLAIM_ID": object,"CLAIM_TYP_CD": object,"SERVICE_DATE": str,"MONTH_ID": int,
                          "DIAGNOSIS_CODE": object,"DIAG_VERS_TYP_ID": int,"DIAG_CD_POSN_NBR": int,"PROVIDER_ID": object,
                          "RESTATE_FLAG": object,"FLEXIBLE_FLD_1_CHAR": object,"FLEXIBLE_FLD_2_CHAR": object}, 
                   sep="|")
diag.sort_values(by=['PATIENT_ID','MONTH_ID','SERVICE_DATE'],ascending=(False,True,True),inplace=True)
diag.reset_index(drop=True,inplace=True)

# read bc_sn_Code
bc_sn_Code =pd.read_csv('BC_SN ICD Code.csv',header=0)
bc_sn_Code.rename(index=str, columns={"diagnosis_cd": "DIAGNOSIS_CODE",'indication_cd':'INDICATION_CODE'},inplace=True)

DIAG_DATA = pd.merge(diag,bc_sn_Code, how="left", on = "DIAGNOSIS_CODE")

DIAG_PATIENT = DIAG_DATA.drop_duplicates(subset=["PATIENT_ID"])

# drop null value: neither BC nor SN
df = DIAG_DATA.drop(DIAG_DATA[pd.isnull(DIAG_DATA['INDICATION_CODE'])].index, inplace=False)
# only consider BC
df = df.loc[df['INDICATION_CODE']=='BC',] 
# get unique patient, also earliest
df3 = df.drop_duplicates(subset = ["PATIENT_ID"])
#rename SERVICE_DATE to BC_DIAG_DATE
df3.rename(index=str, columns={"SERVICE_DATE":"BC_DIAG_DATE"},inplace=True)

DIAG_BC=df3[["PATIENT_ID","CLAIM_ID","BC_DIAG_DATE","INDICATION_CODE"]]

# get sub_indication_cd isn't null, equal to all sn patient
df2 = DIAG_DATA.drop(DIAG_DATA[pd.isnull(DIAG_DATA['sub_indication_cd'])].index,inplace=False)
# get unique patient, also earliest
df4 = df2.drop_duplicates(subset=["PATIENT_ID"])
# rename SERVICE_DATE to SN_DIAG_DATE
df4.rename(index=str, columns={"SERVICE_DATE":"SN_DIAG_DATE"},inplace=True)


DIAG_SN=df4[["PATIENT_ID","CLAIM_ID","SN_DIAG_DATE","sub_indication_cd"]]

DIAG_BC_SN = pd.merge(DIAG_BC,DIAG_SN, how="inner", on = "PATIENT_ID")
DIAG_BC_SN.astype({"BC_DIAG_DATE":"str","SN_DIAG_DATE":"str"}).dtypes
# function days to get the date differences
def days(str1,str2):
    date1=datetime.datetime.strptime(str1,"%m/%d/%Y")
    date2=datetime.datetime.strptime(str2,"%m/%d/%Y")
    num=(date1-date2).days
    return num

# date diff between SN_DIAD_DATE and BC_DIAG_DATE
def date_diff(row):
    day1=row["SN_DIAG_DATE"]
    day2=row["BC_DIAG_DATE"]
    day = days(day1,day2) 
    return day

# define mBC
def mbc_confirm(row):
    if row["DATE_DIFF"] >= -30:
        part1=1
    else:
        part1=0
    return part1
 


def mbc_diag(row):
    if row["DATE_DIFF"] >= 0:
        part1 = row["SN_DIAG_DATE"]
    else:
        part1 = row["BC_DIAG_DATE"]
    return part1



# new column DATE_DIFF
DIAG_BC_SN["DATE_DIFF"]=DIAG_BC_SN.apply(lambda x:date_diff(x),axis=1)

# new column mBC
DIAG_BC_SN["mBC"]=DIAG_BC_SN.apply(lambda x:mbc_confirm(x),axis=1)

diag_mbc = DIAG_BC_SN.loc[DIAG_BC_SN['mBC']== 1,] 

# new column mBC_DIAG_DATE
diag_mbc["mBC_DIAG_DATE"] = diag_mbc.apply(lambda x:mbc_diag(x),axis=1)

DIAG=diag_mbc[["PATIENT_ID","mBC_DIAG_DATE"]]
DIAG_BC_SN2 = DIAG_BC_SN[["PATIENT_ID","DATE_DIFF","mBC"]]

#
DIAG2 = pd.merge(DIAG_BC_SN2,DIAG,how="left",on="PATIENT_ID")

DIAG3 = DIAG_PATIENT[["PATIENT_ID"]]
DIAG_mBC =  pd.merge(DIAG3,DIAG2, how="left", on = "PATIENT_ID")
DIAG_mBC["mBC"].fillna(0,inplace=True)

## Dx_2l
# BC only 
df4.rename(index=str, columns={"SN_DIAG_DATE":"BC_DIAG_DATE","sub_indication_cd":"INDICATION_CODE"},inplace=True)
DIAG_SN=df4[["PATIENT_ID","CLAIM_ID","BC_DIAG_DATE","INDICATION_CODE"]]
df33=DIAG_BC[~DIAG_BC['PATIENT_ID'].isin(DIAG_SN['PATIENT_ID'])].dropna()
# mBC only
dfm=diag_mbc[["PATIENT_ID","CLAIM_ID_y","SN_DIAG_DATE","mBC","DATE_DIFF"]]
dfm.rename(index=str, columns={"CLAIM_ID_y":"CLAIM_ID","SN_DIAG_DATE":"BC_DIAG_DATE","mBC":"INDICATION_CODE"},inplace=True)
def relabel_1 (row):
   if row['INDICATION_CODE'] == 1 :
      return 'mBC'
dfm['INDICATION_CODE'] = dfm.apply (lambda row: relabel_1(row), axis=1)
# SN only
dfmm=diag_mbc[["PATIENT_ID","CLAIM_ID","BC_DIAG_DATE","INDICATION_CODE"]]
df44=DIAG_SN[~DIAG_SN['PATIENT_ID'].isin(dfmm['PATIENT_ID'])].dropna()
df44=df44.iloc[:, 0:4]
# all other
df55 =  pd.concat([dfm,df33,df44], axis=0)
df55["DATE_DIFF"].fillna(0,inplace=True)

DIAG_2l =  pd.merge(DIAG3,df55, how="left", on = "PATIENT_ID")
DIAG_2l["INDICATION_CODE"].fillna('Others',inplace=True)
DIAG_2l["DATE_DIFF"].fillna(0,inplace=True)
DIAG_2l.rename(index=str, columns={"BC_DIAG_DATE":"DIAG_DATE"},inplace=True)
DIAG_2l.to_csv("define diag 2l.csv",index=False)


