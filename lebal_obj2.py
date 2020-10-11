#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 00:41:35 2020

@author: shufei
"""

import os
import pandas as pd
import datetime

os.chdir("/Users/shufei/Novartis/APLD Raw Data/")
dg = pd.read_csv("brand_2l.csv")

dg.sort_values(by=['PATIENT_ID','MONTH_ID','SERVICE_DATE'],ascending=(False,True,True),inplace=True)
dg.reset_index(drop=True,inplace=True)
dg.isna().sum()

df = dg.drop_duplicates(subset=["PATIENT_ID","SERVICE_DATE"])
df.reset_index(drop=True, inplace=True)
df2 = pd.get_dummies(dg, columns=['brand'])

df2_dummy=df2
#['brand_AFI','brand_AI','brand_CHEMO','brand_FAS','brand_IBR','brand_KIS','brand_LET','brand_OTHERS','brand_TAM','brand_VER','brand_XEL']
brand_XEL=df2_dummy.groupby(['PATIENT_ID',"SERVICE_DATE"])['brand_XEL'].agg('sum')
brand_AFI=df2_dummy.groupby(['PATIENT_ID',"SERVICE_DATE"])['brand_AFI'].agg('sum')
brand_AI=df2_dummy.groupby(['PATIENT_ID',"SERVICE_DATE"])['brand_AI'].agg('sum')
brand_CHEMO=df2_dummy.groupby(['PATIENT_ID',"SERVICE_DATE"])['brand_CHEMO'].agg('sum')
brand_FAS=df2_dummy.groupby(['PATIENT_ID',"SERVICE_DATE"])['brand_FAS'].agg('sum')
brand_IBR=df2_dummy.groupby(['PATIENT_ID',"SERVICE_DATE"])['brand_IBR'].agg('sum')
brand_KIS=df2_dummy.groupby(['PATIENT_ID',"SERVICE_DATE"])['brand_KIS'].agg('sum')
brand_LET=df2_dummy.groupby(['PATIENT_ID',"SERVICE_DATE"])['brand_LET'].agg('sum')
brand_TAM=df2_dummy.groupby(['PATIENT_ID',"SERVICE_DATE"])['brand_TAM'].agg('sum')
brand_OTHERS=df2_dummy.groupby(['PATIENT_ID',"SERVICE_DATE"])['brand_OTHERS'].agg('sum')
brand_VER=df2_dummy.groupby(['PATIENT_ID',"SERVICE_DATE"])['brand_VER'].agg('sum')


brand = pd.concat([brand_AFI,brand_AI,brand_CHEMO,brand_FAS,brand_IBR,brand_KIS,brand_LET,brand_OTHERS,brand_TAM,brand_VER,brand_XEL],axis=1)
brand.astype(int).dtypes


brand.reset_index(drop=True,inplace=True)
brand[brand>0] =1

def drug_tag(row):
    a = list(row)
    num_list_new = [str(int(x)) for x in a]
    drug_tag = "".join(num_list_new)
    return drug_tag


brand['DRUG_TAG']=brand.apply(lambda x:drug_tag(x),axis=1)


brand2 = pd.concat([brand,df],axis=1)


#### test
brand2_test = brand2.head(20000)

#brand2_test.drop_duplicates(subset=['PATIENT_ID','DRUG_TAG'],keep='first',inplace=True)


len(brand2_test["PATIENT_ID"].unique())


brand3 = brand2_test[["PATIENT_ID",'DRUG_TAG','SERVICE_DATE']]

brand2_tt = brand3.drop_duplicates(['PATIENT_ID'],keep="first",inplace=False)
#brand2_tt = brand2_tt[["PATIENT_ID",'SERVICE_DATE']]

fin = pd.merge(brand3,brand2_tt,how="left",on="PATIENT_ID")

def days(str1,str2):
    date1=datetime.datetime.strptime(str1,"%m/%d/%Y")
    date2=datetime.datetime.strptime(str2,"%m/%d/%Y")
    num=(date1-date2).days
    return num

def sdate_diff(row):
    day1=row["SERVICE_DATE_x"]
    day2=row["SERVICE_DATE_y"]
    day = days(day1,day2) 
    return day

def brand_diff(row):
    a = row ['DRUG_TAG_x']
    b = row['DRUG_TAG_y']
    if(a == b):
        b_diff = 0
    else:
        b_diff =1
    return b_diff

def obj2_lebal(row):
    if row["DATE_DIFF"]*row['BRAND_DIFF'] >= 30:
        part1 = 1
    else:
        part1 = 0
    return part1

fin["DATE_DIFF"] = fin.apply(lambda x: sdate_diff(x), axis=1)
fin["BRAND_DIFF"] = fin.apply(lambda x:brand_diff(x),axis=1)



fin["y"] = fin.apply(lambda x: obj2_lebal(x),axis=1)
fin2 =fin.drop_duplicates(subset=['PATIENT_ID','y'],inplace=False)

#
#
#fin2.drop(columns=['DRUG_TAG_x','DRUG_TAG_y','SERVICE_DATE_y','DATE_DIFF','MID','BRAND_DIFF'], inplace=True)
#
#fin22 = fin2.loc[fin2['y']== 1,] 
#fin22.rename(index=str, columns={"SERVICE_DATE_x": "SERVICE_DATE"},inplace=True)
#
#
#
#obj2_labeled = pd.merge(brand2_test,fin22,how="left",on="PATIENT_ID")


