# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 13:40:32 2020

@author: 31509
"""

import numpy as np
from sklearn import random_projection
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report as cr
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

result = pd.DataFrame(index=['XGBoo','RF','RP-XGB','RP-RF'],columns=['tn','fp','fn','tp'])

pxrxl = pd.read_csv('pxrxl.csv',header = 0)
pxrxl = pd.get_dummies(pxrxl,columns=['DIAGNOSIS_CODE','DIAG_VERS_TYP_ID','brand','PRC_VERS_TYP_ID','NDC'])

ptlist = pxrxl['PATIENT_ID'].unique()
train, test = train_test_split( ptlist, test_size=0.25, random_state=42)

ptlist = pxrxl['PATIENT_ID'].unique()
train, test = train_test_split( ptlist, test_size=0.25, random_state=42)
print('# of training: ',train.shape[0],'\n','# of testing: ',test.shape[0])

training = pxrxl.loc[pxrxl['PATIENT_ID'].isin(list(train))]
print('# of 1 in train: ',len(training[training['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in train: ',15000-len(training[training['y']==1]['PATIENT_ID'].unique()))
y_train = training['y']
X_train = training.drop(columns=['y','PATIENT_ID','SERVICE_DATE'])

testing = pxrxl.loc[pxrxl['PATIENT_ID'].isin(list(test))]
print('# of 1 in test: ',len(testing[testing['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in test: ',5000-len(testing[testing['y']==1]['PATIENT_ID'].unique()))
testing = testing.sort_values(by=['PATIENT_ID','MONTH_ID'],ascending=(True,True))
testing.shape
y_test = testing['y']
X_test = testing.drop(columns=['y','PATIENT_ID','SERVICE_DATE'])

########################### XGBoosting #############
xgb = XGBClassifier()
xgb.fit(X_train,y_train)
y_pred = xgb.predict(X_test)

tn_1, fp_1, fn_1, tp_1 = confusion_matrix(y_test, y_pred).ravel()
result.iloc[0,0] = tn_1
result.iloc[0,1] = fp_1
result.iloc[0,2] = fn_1
result.iloc[0,3] = tp_1

result.to_csv('result_2.csv')
print(result)

######################### Random Forest #############
clf = RandomForestClassifier()
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
tn_2, fp_2, fn_2, tp_2 = confusion_matrix(y_test, y_pred).ravel()
result.iloc[1,0] = tn_2
result.iloc[1,1] = fp_2
result.iloc[1,2] = fn_2
result.iloc[1,3] = tp_2

result.to_csv('result_2.csv')
print(result)

