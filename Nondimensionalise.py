# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 10:59:36 2021

@author: caraj
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#read in all the data to different dataframes named by date
df_dic = pd.read_excel('Height_data.xlsx', sheet_name = None, header = 1)
count = 0
h_all = []
t_all = []
col_name = []
#merge all the pages
for key in df_dic:
    df = df_dic[key]
    df_h = df.filter(regex='height_cm')
    df_t = df.filter(regex='t_s')

    count_2 = 1
    for col in df_h.columns:
        h_all.append(list(df_h[col]))
        col_name.append(key+'_'+str(count_2))
        count_2 +=1
    for col in df_t.columns:
        t_all.append(list(df_t[col]))
        
H = pd.DataFrame(h_all).T.set_axis(col_name, axis = 1)
T = pd.DataFrame(t_all).T.set_axis(col_name, axis = 1) 

#clear up start times a bit



plt.figure(figsize=(12,7))
plt.plot(T,H)
plt.title('height/time graph of circular vent plumes')
plt.xlabel('time (s)')
plt.ylabel('height (m)')
plt.show()

#%%Non dimensionalised
df = pd.read_excel('Plume_experiments.xlsx', sheet_name = 'exp_details')

#conversions
df['h_conv'] = (df['M']**(0.75))*(df['B']**(-0.5))
df['t_conv'] = df['M']/df['B']

plt.figure(figsize=(12,7))

for exp in col_name:
    h_conv = float(df['h_conv'][df['Name']== exp])
    t_conv = float(df['t_conv'][df['Name']== exp])
    h_nd = (H[exp]/(100*h_conv))#[::8]
    t_nd = (T[exp]/t_conv)#[::8]
    b = df['B'][df['Name']== exp].iloc[0]
    l = f"B = {b:0.1e}"
    if df['noz'][df['Name']==exp].iloc[0] == 'c':
        m = 'o'
    else: 
        m = '+'
    plt.plot(t_nd, h_nd, label = l, linestyle = 'none', marker = m)
    
plt.title('Nondimensionalised height/time graph of circular vent plumes. \n dotted = linear vent, solid = circular vent')
plt.xlabel('time (s) /  M$B^{-1}$ ')
plt.ylabel('height (m) / M$^{0.75}$B$^{-0.5}$')
#plt.xlim([-0.2,8])
plt.legend()
plt.show()

#%% 


