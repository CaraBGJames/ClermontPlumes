# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 14:57:13 2021

@author: caraj
"""
#make a calibration 'curve' for the height of a given exp and save it

import numpy as np
cal = np.zeros(1024)
start_pix = 22
start_val = 0
end_pix = 1024
end_val = 38.5

cal[start_pix:] = np.linspace(start_val, end_val, (end_pix - start_pix))

np.save('Experiments/2021-11-24/cal1',cal)

#%% Check calibration working
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import rotate

file = plt.imread('Experiments/2021-11-24/cal1/cal1000001.tif')
cal = np.load('Experiments/2021-11-24/cal1.npy')

r = list(range(5,45,5))

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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_excel('Height_data.xlsx', '1109', header = 1)
height_pix = df.iloc[:,6].fillna(0).to_numpy().astype(int)
cal = np.load('Experiments/2021-11-09/cal3.npy')

height_cm = np.zeros(len(height_pix))

count = 0
for i in height_pix:
    hm = cal[i]
    height_cm[count] = hm
    count += 1

height_cm[height_cm == 0.] = np.NaN
plt.plot(height_cm)

