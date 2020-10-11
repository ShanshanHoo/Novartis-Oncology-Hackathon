# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 14:17:39 2020

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

result = pd.DataFrame(index=['XGBoo','RF','RP-XGB','RP-RF','SVC','RP-SVC'],columns=['tn','fp','fn','tp'])

pxrx = pd.read_csv('mbc_model_data.csv',header = 0)
pxrx['MONTH_DIFF']=(pxrx['MONTH_DIFF']-pxrx['MONTH_DIFF'].mean())/pxrx['MONTH_DIFF'].std()
pxrx['UNIT_OF_SVC_AMT']=(pxrx['UNIT_OF_SVC_AMT']-pxrx['UNIT_OF_SVC_AMT'].mean())/pxrx['UNIT_OF_SVC_AMT'].std()
pxrx = pd.get_dummies(pxrx,columns=['DIAGNOSIS_CODE','DIAG_VERS_TYP_ID','brand','PRC_VERS_TYP_ID'])

print('# of mbc patients: ',len(pxrx[pxrx['y']==1]['PATIENT_ID'].unique()))
print('# of non-mbc patients: ',len(pxrx['PATIENT_ID'].unique())-len(pxrx[pxrx['y']==1]['PATIENT_ID'].unique()))

ptlist = pxrx['PATIENT_ID'].unique()
train, test = train_test_split( ptlist, test_size=0.25, random_state=42)
print('# of training: ',train.shape[0],'\n','# of testing: ',test.shape[0])

training = pxrx.loc[pxrx['PATIENT_ID'].isin(list(train))]
print('# of 1 in train: ',len(training[training['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in train: ',15000-len(training[training['y']==1]['PATIENT_ID'].unique()))
y_train = training['y']
X_train = training.drop(columns=['y','PATIENT_ID','MONTH_ID','index'])
testing = pxrx.loc[pxrx['PATIENT_ID'].isin(list(test))]
print('# of 1 in test: ',len(testing[testing['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in test: ',5000-len(testing[testing['y']==1]['PATIENT_ID'].unique()))

testing = testing.sort_values(by=['PATIENT_ID','MONTH_ID'],ascending=(True,True))
print('# of 1 in test: ',len(testing[testing['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in test: ',5000-len(testing[testing['y']==1]['PATIENT_ID'].unique()))
testing=testing.drop_duplicates(subset=['PATIENT_ID','y'],keep='first')
print('# of 1 in test: ',len(testing[testing['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in test: ',5000-len(testing[testing['y']==1]['PATIENT_ID'].unique()))
testing.drop_duplicates(subset=['PATIENT_ID'],keep='last',inplace=True)
print('# of 1 in test: ',len(testing[testing['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in test: ',5000-len(testing[testing['y']==1]['PATIENT_ID'].unique()))
testing.shape
y_test = testing['y']
X_test = testing.drop(columns=['y','PATIENT_ID','MONTH_ID','index'])

########################### XGBoosting #############
xgb = XGBClassifier()
xgb.fit(X_train,y_train)
y_pred = xgb.predict(X_test)

tn_1, fp_1, fn_1, tp_1 = confusion_matrix(y_test, y_pred).ravel()
result.iloc[0,0] = tn_1
result.iloc[0,1] = fp_1
result.iloc[0,2] = fn_1
result.iloc[0,3] = tp_1

######################### Random Forest #############
clf = RandomForestClassifier()
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
tn_2, fp_2, fn_2, tp_2 = confusion_matrix(y_test, y_pred).ravel()
result.iloc[1,0] = tn_2
result.iloc[1,1] = fp_2
result.iloc[1,2] = fn_2
result.iloc[1,3] = tp_2

####################### RP-XGBoosting ###############
transformer = random_projection.SparseRandomProjection(eps=0.6)
X_train_rp = transformer.fit_transform(X_train)
xgb = XGBClassifier()
xgb.fit(X_train_rp,y_train)
X_test_rp=transformer.transform(X_test)
y_pred = xgb.predict(X_test_rp)
tn_3, fp_3, fn_3, tp_3 = confusion_matrix(y_test, y_pred).ravel()
result.iloc[2,0] = tn_3
result.iloc[2,1] = fp_3
result.iloc[2,2] = fn_3
result.iloc[2,3] = tp_3

####################### RP-Random Forest ###############
transformer = random_projection.SparseRandomProjection(eps=0.6)
X_train_rp = transformer.fit_transform(X_train)
clf = RandomForestClassifier()
clf.fit(X_train_rp,y_train)
X_test_rp=transformer.transform(X_test)
y_pred = clf.predict(X_test_rp)
tn_4, fp_4, fn_4, tp_4 = confusion_matrix(y_test, y_pred).ravel()
result.iloc[3,0] = tn_4
result.iloc[3,1] = fp_4
result.iloc[3,2] = fn_4
result.iloc[3,3] = tp_4

############################# SVC ################
clf = SVC(gamma='auto',C=0.5)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
tn_5, fp_5, fn_5, tp_5 = confusion_matrix(y_test, y_pred).ravel()
result.iloc[4,0] = tn_5
result.iloc[4,1] = fp_5
result.iloc[4,2] = fn_5
result.iloc[4,3] = tp_5

############################ RP-SVC #############
transformer = random_projection.SparseRandomProjection(eps=0.6)
X_train_rp = transformer.fit_transform(X_train)
clf = SVC(gamma='auto',C=0.5)
clf.fit(X_train_rp,y_train)
X_test_rp=transformer.transform(X_test)
y_pred = clf.predict(X_test_rp)
tn_6, fp_6, fn_6, tp_6 = confusion_matrix(y_test, y_pred).ravel()
result.iloc[5,0] = tn_6
result.iloc[5,1] = fp_6
result.iloc[5,2] = fn_6
result.iloc[5,3] = tp_6


result.to_csv('result_obj1.csv')