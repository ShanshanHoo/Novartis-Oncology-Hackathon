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


result = pd.DataFrame(index=['XGBoo','RF','RP-XGB','RP-RF'],columns=['tn','fp','fn','tp'])

y = pxrx['y']
X = pxrx.drop(columns=['y','PATIENT_ID','MONTH_ID'])
X = pd.get_dummies(X,columns=['DIAGNOSIS_CODE','DIAG_VERS_TYP_ID','brand','PRC_VERS_TYP_ID'])
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.25, random_state=42)

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

result.to_csv('result_obj1.csv')