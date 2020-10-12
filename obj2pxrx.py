# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 12:09:57 2020

@author: Shanshan Hu
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
import re

os.chdir("/Users/conta/Documents/Novartis")
## Process Dx
diag = pd.read_csv('DIAG_2l.txt', 
                   dtype={"PATIENT_ID": int,"CLAIM_ID": object,"CLAIM_TYP_CD": object,"SERVICE_DATE": str,"MONTH_ID": int,
                          "DIAGNOSIS_CODE": object,"DIAG_VERS_TYP_ID": int,"DIAG_CD_POSN_NBR": int,"PROVIDER_ID": object,
                          "RESTATE_FLAG": object,"FLEXIBLE_FLD_1_CHAR": object,"FLEXIBLE_FLD_2_CHAR": object}, 
                   sep="|")

# read bc_sn_Code
bc_sn_Code =pd.read_csv('BC_SN ICD Code.csv',header=0)
bc_sn_Code.rename(index=str, columns={"diagnosis_cd": "DIAGNOSIS_CODE",'indication_cd':'INDICATION_CODE'},inplace=True)

diag_c = pd.merge(diag,bc_sn_Code, how="left", on = "DIAGNOSIS_CODE")
#diag_c = diag_c.drop_duplicates(subset=["PATIENT_ID"])

## merge rx_px_combine with drug reference, add brand
prx = pd.read_csv('rx_px_combine_2l.csv', header=0)

dg_rf = pd.read_csv('Drug Reference1.csv', dtype={"drug_id ": str,"drug_name": str,"drug_generic_name": str},header=0)
dg_rf = dg_rf[dg_rf.columns[0:3]] 
dg_rf = dg_rf.rename(columns={"drug_id ":"drug_id"})
dg_rf.head()
dg=pd.merge(prx,dg_rf,how='left',on='drug_id',validate="m:1")

dg.to_csv("drug_pxrx_2l.csv", index = False)

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
dg['brand'] = dg.apply (lambda row: label_brand(row), axis=1)
dg.to_csv("brand_2l.csv", index = False)

#sort by date
dg = pd.read_csv('brand_2l.csv', header=0)
dg.sort_values(by=['PATIENT_ID','SERVICE_DATE'],ascending=(False,True),inplace=True)
dg.reset_index(drop=True,inplace=True)
dg.isna().sum()
dg.drop(columns=['drug_name','drug_generic_name'],inplace=True)

# define 1st line treatment
#dg.drop(columns=['drug_id','drug_name','drug_generic_name'],inplace=True)
df1 = dg.drop_duplicates(subset = ["PATIENT_ID"])
df1.drop(columns=['CLAIM_ID','MONTH_ID','drug_id','DIAGNOSIS_CODE','brand'],inplace=True)

df=pd.merge(df1,dg,how='left',on=['PATIENT_ID','SERVICE_DATE'])
df.shape # (348663, 7)
df.drop(columns=['CLAIM_ID','MONTH_ID','drug_id','DIAGNOSIS_CODE'],inplace=True)
df2 = pd.get_dummies(df, columns=['brand'])

df2_dummy=df2
#['brand_AFI','brand_AI','brand_CHEMO','brand_FAS','brand_IBR','brand_KIS','brand_LET','brand_OTHERS','brand_TAM','brand_VER','brand_XEL']
df2_dummy['brand_XEL']=df2_dummy.groupby(['PATIENT_ID'])['brand_XEL'].transform('sum')
df2_dummy['brand_AFI']=df2_dummy.groupby(['PATIENT_ID'])['brand_AFI'].transform('sum')
df2_dummy['brand_AI']=df2_dummy.groupby(['PATIENT_ID'])['brand_AI'].transform('sum')
df2_dummy['brand_CHEMO']=df2_dummy.groupby(['PATIENT_ID'])['brand_CHEMO'].transform('sum')
df2_dummy['brand_FAS']=df2_dummy.groupby(['PATIENT_ID'])['brand_FAS'].transform('sum')
df2_dummy['brand_IBR']=df2_dummy.groupby(['PATIENT_ID'])['brand_IBR'].transform('sum')
df2_dummy['brand_KIS']=df2_dummy.groupby(['PATIENT_ID'])['brand_KIS'].transform('sum')
df2_dummy['brand_LET']=df2_dummy.groupby(['PATIENT_ID'])['brand_LET'].transform('sum')
df2_dummy['brand_TAM']=df2_dummy.groupby(['PATIENT_ID'])['brand_TAM'].transform('sum')
df2_dummy['brand_OTHERS']=df2_dummy.groupby(['PATIENT_ID'])['brand_OTHERS'].transform('sum')
df2_dummy['brand_VER']=df2_dummy.groupby(['PATIENT_ID'])['brand_VER'].transform('sum')
df2_dummy.sort_values(by=['PATIENT_ID','SERVICE_DATE','brand_AFI','brand_AI','brand_CHEMO','brand_FAS','brand_IBR','brand_KIS','brand_LET','brand_OTHERS','brand_TAM','brand_VER','brand_XEL'],ascending=(False,True,True,True,True,True,True,True,True,True,True,True,True),inplace=True)
df3=df2_dummy.drop_duplicates(subset = ["PATIENT_ID"])



df.shape
df.columns
len(df["PATIENT_ID"].unique())
len(df["SERVICE_DATE"].unique())
len(df["CLAIM_ID"].unique())
len(df["drug_id"].unique())
len(df["DIAGNOSIS_CODE"].unique())
len(df["drug_name"].unique())
len(df["drug_generic_name"].unique())
len(df["brand"].unique())



