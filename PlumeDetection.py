# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:41:05 2021

@author: caraj
"""

from height_find import height_find
import matplotlib.pyplot as plt
from skimage.transform import rotate
import glob
import time

import matplotlib.pyplot as plt
import numpy as np
import pywt
from skimage.filters import threshold_otsu
from skimage.morphology import binary_opening, binary_closing, binary_dilation, area_opening
from skimage.morphology import square
from skimage.morphology import remove_small_holes
from skimage.measure import label
from skimage.feature import canny

def getLargestCC(segmentation):
    labels = label(segmentation)
    if ( labels.max() != 0 ): # assume at least 1 CC
        largestCC = labels == np.argmax(np.bincount(labels.flat)[1:])+1
    else:
        largestCC = np.zeros(segmentation.shape)
    return largestCC

#%% RunCOde
t0 = time.time()

directory = 'Experiments/2021-11-17'
exp_n = '1'
I_ref = plt.imread(directory+'/back'+exp_n+'/back'+exp_n+'000001.tif')

filenames = glob.glob(directory+'/exp'+exp_n+'/exp'+exp_n+'*.tif')
n = len(filenames)
dt = 10

T = list(range(100, n-dt, 10))
H = np.zeros(len(T))
count = 0
for t in T:
    #read in the images
    I_t =  plt.imread(
        directory+'/exp'+exp_n+'/exp'+exp_n+str(t).zfill(6)+'.tif')
    I_step = plt.imread(
        directory+'/exp'+exp_n+'/exp'+exp_n+str(t+dt).zfill(6)+'.tif')
    
    #find height
    h = height_find(I_t, I_step, I_ref)
    H[count] = h
    count +=1
    p = count/len(T)*100
    if count%20==0:
        print(p)
        im2 = rotate(I_t,-90, resize = True)
        plt.figure(figsize = (18,18))
        plt.imshow(im2, cmap = 'Greys_r', vmin = 0, vmax = 0.005)
        plt.axhline((1024-h), color = 'w', linewidth = 1)
        plt.axis('off')
        plt.show()
        

plt.plot(T,H)

t1 = time.time()
print('time = '+ str(t1-t0))
    
#%% Test working
directory = 'Experiments/2021-11-16'
exp_n = '1'
t = 500
dt = 30


I_t =  plt.imread(directory+'/exp'+exp_n+'/exp'+exp_n+str(t).zfill(6)+'.tif')
I_step = plt.imread(directory+'/exp'+exp_n+'/exp'+exp_n+str(t+dt).zfill(6)+'.tif')
I_ref = plt.imread(directory+'/exp'+exp_n+'/exp'+exp_n+'000001.tif')

h = height_find(I_t, I_step, I_ref)

im = I_t.copy()
im[:,1024-h] = np.max(im)
im2 = rotate(im,-90, resize = True)
plt.figure(figsize = (18,18))
plt.imshow(im2, cmap = 'Greys_r', vmin = 0, vmax = 0.005)
plt.axis('off')
plt.show()
print(h)

#%% Test

directory = 'Experiments/2021-11-17'
exp_n = '1'
t = 649
dt = 50

I_t =  plt.imread(directory+'/exp'+exp_n+'/exp'+exp_n+str(t).zfill(6)+'.tif')
I_step = plt.imread(directory+'/exp'+exp_n+'/exp'+exp_n+str(t+dt).zfill(6)+'.tif')
I_ref = plt.imread(directory+'/exp'+exp_n+'/exp'+exp_n+'000001.tif')

A = I_t - I_step
A[I_t < I_step] = 0 
B = I_t - I_ref
B[I_t < I_ref] = 0

#wavelet transform
coeffs2_a = pywt.dwt2(A, wavelet = 'db1')
coeffs2_b = pywt.dwt2(B, wavelet = 'db1')
A2, (LH, HL, HH) = coeffs2_a
B2, (lh, hl, hh) = coeffs2_b

#reconstruct
A3 = pywt.waverec2(coeffs2_a, 'db1')
B3 = pywt.waverec2(coeffs2_b, 'db1')

#get rid of top 1% brightest values and otsu thresh
b = np.sort(B3[B3!=0].flatten())
thr = b[int(len(b) - len(b)/1000)]
A3[A3>=thr] = np.mean(b)
B3[B3>=thr] = np.mean(b)

thresh_a = threshold_otsu(A3)
thresh_b = threshold_otsu(B3)
A4 = A3>thresh_a
B4 = B3>thresh_b

#clean background of pixels smaller than 1pix, connect > 5 pix
A5 = binary_opening(A4)
B5 = binary_opening(B4)
A6 = binary_closing(A5, square(3))
B6 = binary_closing(B5, square(3))

#combine the two mask 
C = A6 + B6

#get the biggest 
D = getLargestCC(C)

E = binary_dilation(D, square(3))
    
#and finally find the top height from the base
if np.sum(E) < 200:
    F = 1024
else:
    F = 1024 - np.argmax(np.sum(E, axis = 0) != 0)

G = canny(E)

im = I_t.copy()
im[G] = np.max(im)
im2 = rotate(im,-90, resize = True)
plt.figure(figsize = (18,18))
plt.imshow(im2, cmap = 'Greys_r', vmin = 0, vmax = 0.005)
plt.axhline((1024-F), color = 'w', linewidth = 1)
plt.axis('off')
plt.show()
#%% Saving data
directory = 'Experiments/2021-11-17'
exp_n = '1'

for f in range(100, 2800, 10):
    name = directory+'/exp'+exp_n+'/exp'+exp_n+str(f).zfill(6)+'.tif'
    I_t = plt.imread(name)
    plt.imshow(I_t, vmin = 0, vmax = 300)
    plt.axis('off')
    plt.show()

