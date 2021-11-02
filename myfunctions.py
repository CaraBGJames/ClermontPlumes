# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 14:24:53 2021

@author: caraj
"""

import matplotlib.pyplot as plt
from skimage.transform import rotate
import numpy as np
import copy
from scipy.signal import lfilter
from skimage.filters import threshold_yen
from skimage.exposure import equalize_adapthist
import matplotlib.colors as colors
from skimage.morphology import binary_erosion as b_e
from skimage.morphology import diamond
from scipy.signal import savgol_filter

def show_im(image, cmap_type = 'Greys_r', title=''):
    """shows image as plot"""
    im = rotate(image,-90, resize = True)
    im_sum = np.sum(im)
    plt.imshow(im, cmap = cmap_type, vmin = 0, vmax = 0.001)
    plt.title(title)
    plt.axis('off')
    plt.colorbar()
    plt.show()

def find_top(image):
    """Find the top of the plume image"""
    thresh = np.sum(image)**(1/3.5)
    binary = image > thresh
    binary2 = b_e(binary, diamond(1))
    tot = np.sum(binary2)
    if tot < 20:
        top = 0
    else:
        top = np.where(np.sum(binary2,0) !=0)[0][0]
    return (1023 - top)
  
def show_frame_top(array, frame_num):
    """returns image of one frame in an array where frames are 3rd dimension
    and also puts a line at where the top is calulated"""
    frame = array[:, :, frame_num]
    top = find_top(frame)   
    im = rotate(frame,-90, resize = True)
    plt.imshow(im, cmap = 'Greys_r', vmin=0, vmax=0.01)
    plt.axhline((1023-top), color = 'w', linewidth = 1)
    plt.axis('off')
    plt.show()
    
def plume_height(array):
    """returns a graph of how the height of the plume images vary with time"""
    #finding height in pix
    height_arr = []
    count = 0
    for n in range(array.shape[2]):
        h = find_top(array[:,:,n])
        height_arr.append(h)
        if count % 100 == 0:
            print(count)
        count+=1
        
    return np.array(height_arr)

def plot_height(height_vals, raw = True, raw_col = 'k', smooth = True, smooth_col = 'r'):
    """plots the height with revised axis and smoothed"""
    if raw == True: 
        plt.plot(height_vals, linewidth = 1, c = raw_col)
        
    if smooth == True:
        height_smooth = savgol_filter(height_vals, 401, 3) # window size 51, polynomial order 3
        plt.plot(height_smooth, linewidth = 2, c = smooth_col)
    #sorting out the axis
    xtick_val = np.arange(0,41,5)
    xtick_loc = np.multiply(xtick_val,125)
    
    height = np.concatenate((np.zeros(13), np.linspace(0,76,1024-13)))
    ytick_val = np.arange(0,80,10)
    ytick_loc = [14]
    
    for n in ytick_val[1:]:
        idx = np.abs(height - n).argmin()
        ytick_loc.append(idx)
        yticks = np.array(ytick_loc)
    
    plt.ylabel('height, cm')
    plt.xlabel('time, s')
    plt.yticks(yticks,ytick_val)
    plt.xticks(xtick_loc,xtick_val)
    
def hist(image, nbins = 256):
    """Plot a histogram of the pixel variation in image"""
    hist, bin_edges = np.histogram(image, bins = nbins)
    plt.bar(bin_edges[:-1], hist, width = 1)
    plt.xlim(min(bin_edges), max(bin_edges))
    plt.show()
    
def to_8bit(image):
    """converts a 16bit to 8bit image"""
    if image.dtype == 'uint16':
        import cv2
        im_8 = cv2.convertScaleAbs(image, alpha=255/image.max())
        return im_8
    else:
        print('Image must be in uint16 format')
        
def remove_back(image, back):
    """Remove the background image of plume"""
    removed = image - back
    #make sure it doesn't loop around and get rid of low variation
    removed[(back > image)] = 0
    return removed