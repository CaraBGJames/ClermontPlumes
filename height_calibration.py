# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 14:57:13 2021

@author: caraj
"""
#make a calibration 'curve' for the height of a given exp and save it

import numpy as np
cal = np.zeros(1024)
start_pix = 15
start_val = 0
end_pix = 1024
end_val = 54.7

cal[start_pix:] = np.linspace(start_val, end_val, (end_pix - start_pix))

#np.save('Experiments/2021-11-15/cal3',cal)

#%% Check calibration working
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import rotate

file = plt.imread('Experiments/2021-10-21/cal1/cal1000001.tif')
cal = np.load('Experiments/2021-10-21/cal1.npy')

r = list(range(5,80,5))

h = np.zeros(len(r))
count = 0
for f in r :
    dif = np.abs(cal - f)
    h[count] = 1024 - dif.argmin()
    count+=1
     
im = rotate(file,-90, resize = True)
plt.figure(figsize = (24,24))
plt.imshow(im, cmap = 'Greys_r')
for n in range(len(h)):
    plt.axhline((h[n]), color = 'r', linewidth = 1)
#plt.axis('off')
plt.show()
    
#%%import height data and translate it

import pandas as pd
df = pd.read_excel('Height_data.xlsx', '1115')
height_pix = df.iloc[1:,1].dropna().to_numpy().astype(int)
cal = np.load('Experiments/2021-11-15/cal1.npy')

height_cm = np.zeros(len(height_pix))

count = 0
for i in height_pix:
    hm = cal[i]
    height_cm[count] = hm
    count += 1

plt.plot(height_cm)

