import numpy as np
from sklearn import random_projection
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report as cr
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import resample
import pandas as pd
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
import os
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
import re
import datetime
result = pd.DataFrame(index=['XGBoo'],columns=['tn','fp','fn','tp'])

pxrx = pd.read_csv('trt_model_data_test2.csv',header = 0)
pxrx=pxrx.drop(columns=['brand_AFI_x',
       'brand_AI_x', 'brand_CHEMO_x', 'brand_FAS_x', 'brand_IBR_x',
       'brand_KIS_x', 'brand_LET_x', 'brand_OTHERS_x', 'brand_TAM_x',
       'brand_VER_x', 'brand_XEL_x','1st_DIAG_DATE', '2nd_DIAG_DATE', 'DIAG_DATE','BRAND_DIFF', 'DIAG_DATE_DIFF', 'TRT_DATE_DIFF'])
#,'INDICATION_CODE', 'DIAG_DATE_DIFF', 'TRT_DATE_DIFF'
pxrx = pd.get_dummies(pxrx, columns=['INDICATION_CODE'])

train, test = train_test_split(pxrx['PATIENT_ID'].unique(), test_size=0.25, random_state=42)
#patient_1 = list(pxrx[pxrx['y']==1]['PATIENT_ID'])
#patient_0 = list(pxrx[pxrx['y']==0]['PATIENT_ID'])
#train_1, test_1 = train_test_split( patient_1, test_size=0.25, random_state=42)
#train_0, test_0 = train_test_split( patient_0, test_size=0.25, random_state=42)
#
#train = train_1+train_0
#test = test_1+test_0



training = pxrx.loc[pxrx['PATIENT_ID'].isin(list(train))]
print('# of 1 in train: ',len(training[training['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in train: ',15000-len(training[training['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in train: ',len(training[training['y']==0]['PATIENT_ID'].unique()))
y_train = training['y']
X_train = training.drop(columns=['y','PATIENT_ID'])
testing = pxrx.loc[pxrx['PATIENT_ID'].isin(list(test))]
print('# of 1 in test: ',len(testing[testing['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in test: ',5000-len(testing[testing['y']==1]['PATIENT_ID'].unique()))
print('# of 0 in test: ',len(testing[testing['y']==0]['PATIENT_ID'].unique()))
testing.shape
y_test = testing['y']
X_test = testing.drop(columns=['y','PATIENT_ID'])

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
result.iloc[0,0] = tn_2
result.iloc[0,1] = fp_2
result.iloc[0,2] = fn_2
result.iloc[0,3] = tp_2

result.to_csv('result_obj2_test2_test.csv')
