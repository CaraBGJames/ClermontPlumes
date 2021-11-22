# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 13:57:41 2021

@author: caraj
"""

# %% Importing and defining functions and experiment number
import matplotlib.pyplot as plt
from skimage.exposure import equalize_adapthist
import glob
import numpy as np
import time
import myfunctions as mf
import cv2

directory = 'Experiments/2021-11-17'
exp_n = '1'

# %% Background average

back_files = glob.glob(directory+'/back'+exp_n+'/back'+exp_n+'*.tif')
file1 = plt.imread(back_files[0])
height, width = file1.shape
back_array = np.zeros((height, width, len(back_files)), dtype = 'uint16')
count = 0
for file in back_files:
    back = plt.imread(file)
    back_array[:, :, count] = back
    count += 1

back_av = np.uint16(np.mean(back_array, axis = 2))

# %% Saving all the images into an array
t0 = time.time()

filenames = glob.glob(directory+'/exp'+exp_n+'/exp'+exp_n+'*.tif')
file1 = plt.imread(filenames[0])
height, width = file1.shape
img_array = np.zeros((height, width, len(filenames)), dtype = 'uint16')
count = 0

for file in filenames:
    img = plt.imread(file)
    
    #comment out _noback if needed
    img_noback = mf.remove_back(img, back_av)
    img_array[:, :, count] = img_noback
    
    count += 1
    if count%100 == 0:
        print(count)

t1 = time.time()
print(t1-t0)

name = '/2021-11-17_exp1_noback'
np.save(directory+name,img_array)
# %% change to 8bit and save
img_array_8 = np.zeros((img_array.shape), dtype = 'uint8')
count = 0
for f in range(img_array.shape[2]):
    f_16 = img_array[:,:,f]
    f_8 = mf.to_8bit(f_16)
    img_array_8[:, :, f] = f_8
    if count % 100 == 0:
        print(count)
    count+=1

name = '2021-10-21_exp3_8bit_noback'
np.save(directory+name,img_array_8)

#%% Load info from excel

import pandas as pd

xls = pd.ExcelFile('Plume_roundnozzle.xlsx')
df2 = pd.read_excel(xls, 'Sheet3')
B = df2['B m4/s3'].to_numpy()
