# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 21:58:51 2020

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

dg = pd.read_csv('drug_pxrx_2l.csv', header=0)

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
