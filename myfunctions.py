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

def show_im(image, cmap_type = 'viridis', title=''):
    """shows image as plot"""
    im = rotate(image,-90, resize = True)
    plt.imshow(im, cmap = cmap_type)
    plt.title(title)
    plt.axis('off')
    plt.show()
    
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
        
def remove_back(image, back, value = 10):
    """Remove the background image of plume"""
    removed = image - back
    #make sure it doesn't loop around and get rid of low variation
    removed[(back > image) | (removed < value)] = 0
    return removed

def find_top(image, thresh = 70):
    """Find the top of the plume image"""
    binary = image > thresh
    total = binary.sum()
    if total < 100:
        top = 0
    else:
        top = np.where(sum(binary) > 0)[0][0]
    return top
  
def show_frame_top(array, frame_num, val = 100):
    """returns image of one frame in an array where frames are 3rd dimension
    and also puts a line at where the top is calulated"""
    frame = copy.deepcopy(array[:, :, frame_num])
    top = find_top(frame, val)   
    im = rotate(frame,-90, resize = True)
    plt.imshow(im, cmap = 'Greys_r')
    plt.axhline(top, color = 'w', linewidth = 1)
    plt.axis('off')
    plt.show()
    
def plume_height(array, val = 150):
    """returns a graph of how the height of the plume images vary with time"""
    #finding height in pix
    height_arr = []
    count = 0
    for n in range(array.shape[2]):
        h = find_top(array[:,:,n], val)
        height_arr.append(h)
        if count % 100 == 0:
            print(count)
        count+=1
    return height_arr

def plot_height(height_vals, smooth = True, smooth_val = 150):
    #plotting
    plt.plot(height_vals, linewidth = 1, c = 'k')
    if smooth == True:
        n = smooth_val  # the larger n is, the smoother curve will be
        b = [1.0 / n] * n
        a = 1
        yy = lfilter(b, a, height_vals)
        plt.plot(yy, linewidth=2, linestyle="-", c="r")  # smooth by filter
    
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
    plt.show()
    