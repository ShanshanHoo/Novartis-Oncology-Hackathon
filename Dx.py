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

# define BC SN---- see attached 'BC_SN ICD CODE.xlsx'
bc_sn_Code = pd.read_csv('E:\\Hackathon_project\\rawdata\\BC_SN ICD CODE.csv',header=0)
bc_sn_Code.columns
bc_sn_Code.rename(index=str, columns={"diagnosis_cd": "DIAGNOSIS_CODE",'indication_cd':'INDICATION_CODE'},inplace=True)
DIAG_data = pd.merge(DIAG_data,bc_sn_Code,how='left',on='DIAGNOSIS_CODE')


