# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 10:53:20 2020

@author: 31509
"""

import pandas as pd
import numpy as np
import seaborn as sns #visualisation
import matplotlib.pyplot as plt #visualisation

# import data, sort by ascending time 
DIAG_data = pd.read_csv('E:\\Hackathon_project\\rawdata\\DIAG.txt',sep='|',header=0)
DIAG_data.sort_values(by=['PATIENT_ID','MONTH_ID','SERVICE_DATE'],ascending=(False,True,True),inplace=True)
DIAG_data.reset_index(drop=True,inplace=True)

# define BC ---- see attached 'BC_SN ICD CODE.xlsx'
bc_sn_Code = pd.read_csv('E:\\Hackathon_project\\rawdata\\BC_SN ICD CODE.csv',header=0)
bc_sn_Code.columns
bc_sn_Code.rename(index=str, columns={"diagnosis_cd": "DIAGNOSIS_CD",'indication_cd':'INDICATION_CODE'},inplace=True)
#DIAG_data['INDICATION_CODE']=DIAG_data.apply(lambda x: 'BC' if x.DIAGNOSIS_CODE in bc_sn_Code['DIAGNOSIS_CD'].values, axis=1) 不懂这个为啥不行


for i in range(DIAG_data.shape[0]):
    if DIAG_data['DIAGNOSIS_CODE'][i] in bc_sn_Code['DIAGNOSIS_CD'].values[0:46]:
        DIAG_data['INDICATION_CODE'] = 'BC'
    elif DIAG_data['DIAGNOSIS_CODE'][i] in bc_sn_Code['DIAGNOSIS_CD'].values[46:]:
        DIAG_data['INDICATION_CODE'] = 'SN'


print('unmber of patient: ',len(list(DIAG_data['PATIENT_ID'].unique())))
patient_ID = list(DIAG_data['PATIENT_ID'].unque()) # list of patient id


