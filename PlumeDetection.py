# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:41:05 2021

@author: caraj
"""

import matplotlib.pyplot as plt
import numpy as np
import pywt
from skimage.filters import threshold_otsu
from skimage.filters import gaussian
from skimage.morphology import area_opening
from skimage.morphology import binary_closing

I_t =  plt.imread('exp1001000.tif')
I_step = plt.imread('exp1001010.tif')
I_ref = plt.imread('exp1000001.tif')

#differences and get rid of ones with high values
I_t > I_step
A = I_t - I_step
A[I_t < I_step] = 0
B = I_t - I_ref
B[I_t < I_ref] = 0

#wavelet transform
coeffs2_a = pywt.dwt2(A, wavelet = 'db1')
coeffs2_b = pywt.dwt2(B, wavelet = 'db1')
A2, (LH, HL, HH) = coeffs2_a
B2, (lh, hl, hh) = coeffs2_b
fig = plt.figure(figsize=(12, 3))
plt.imshow(A2)

#reconstruct and low pass filter
A3 = pywt.waverec2(coeffs2_a, 'db1')
B3 = pywt.waverec2(coeffs2_b, 'db1')

#otsu thresh
thresh_a = threshold_otsu(A3)
thresh_b = threshold_otsu(B3)
A4 = A3>thresh_a
B4 = B3>thresh_b

#clean background of pixels smaller than 1pix, connect > 5 pix
#NOT WORKING
A5 = area_opening(A4, 1)
B5 = area_opening(B4, 1)
A6 = binary_closing(A5)
B6 = binary_closing(B5)

#combine the two mask 
C = A6 + B6

#get the biggest 

