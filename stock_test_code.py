# -*- coding: utf-8 -*-
"""
Created on Sun May  3 00:25:54 2020

@author: Bruce
"""
import time
import datetime as dt   
import requests
from io import StringIO
import pandas as pd
import numpy as np

def dateselec(manual : bool = False, dateinput : str = '20200604')->str:
    if manual == False :
        timenow = time.localtime()
        date = timenow[:3]
        md = ''.join(['0'+str(i) for i in date if i <10])
        datestr = ''.join([str(date[0]), md])
    else:
        datestr = dateinput    
    return datestr

    
# download the data
    
manualSeleddate = True
date = '20200430'
r= requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + dateselec(manualSeleddate, date) + '&type=ALL')

# to dateframe
df = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\r\n")].index(True)-1)
df = df.iloc[:,1:16]

# dateframe formate arrangement：
df = df.apply(lambda s: pd.to_numeric(s.astype(str).str.replace(",", "").replace("+", "1").replace("-", "-1"), errors = 'ignore'))

# selection
df_sele = df[df.loc[:,'本益比'] > 10]
