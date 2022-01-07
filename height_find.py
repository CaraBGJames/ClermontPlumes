# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 13:24:44 2021

@author: caraj
"""
import numpy as np
import pywt
from skimage.filters import threshold_otsu
from skimage.morphology import binary_opening, binary_closing, binary_dilation
from skimage.morphology import square, area_opening
from skimage.measure import label

def getLargestCC(segmentation):
    labels = label(segmentation)
    if ( labels.max() != 0 ): # assume at least 1 CC
        largestCC = labels == np.argmax(np.bincount(labels.flat)[1:])+1
    else:
        largestCC = np.zeros(segmentation.shape)
    return largestCC

def plume_find(I_t, I_step, I_ref):
    """Returns binary image array of the detected plume at frame I_t
    
    Keyword arguments:
    I_t: the 2D image array at time t
    I_step: the 2D image array at time t + dt
    I_ref: the background 2D image
    
    """
    #differences and get rid of ones with high values
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

    #get rid of brightest 1% pix and otsu thresh
    b = np.sort(B3[B3!=0].flatten())
    thr = b[int(len(b) - len(b)/1000)]
    A3[A3>=thr] = np.mean(b)
    B3[B3>=thr] = np.mean(b)
    
    thresh_a = threshold_otsu(A2)
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

    #Dilate and fill holes
    E = binary_dilation(D, square(3))
    
    return E
  
def height_find(I_t, I_step, I_ref):
    """find the height of the plume in pixels from base of image
    
    Keyword arguments:
    I_t: the 2D image array at time t
    I_step: the 2D image array at time t + dt
    I_ref: the background 2D image
    
    returns the height in pixels from the base
    """
    E = plume_find(I_t, I_step, I_ref):
    
    #and finally find the top height from the base
    if np.sum(E) < 100:
        F = np.NaN
    else:
        F = 1024 - np.argmax(np.sum(E, axis = 0) != 0)
    
    return F
