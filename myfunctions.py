# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 14:24:53 2021

@author: caraj
"""

import matplotlib.pyplot as plt
from skimage.transform import rotate
import numpy as np
from skimage.morphology import binary_erosion as b_e
from skimage.morphology import diamond
from scipy.signal import savgol_filter

def show_im(image, cmap_type = 'Greys_r', title=''):
    """Rotate and show an image array as plot.
    
    Keyword arguments:
    image: the 2D image array
    cmap_type: colormap (default = Greys_r)
    title: plot title (default = none)
    """
    im = rotate(image,-90, resize = True)
    plt.imshow(im, cmap = cmap_type)
    plt.title(title)
    plt.axis('off')
    plt.colorbar()
    plt.show()

def find_top(image):
    """Find the height in pixels of the plume from an image.
    
    Use an arbitrary threshold relating to the total image brightness
    to form a binary image. Remove noise using erosion. If total brightness
    very low, count as having no plume. Sum along the columns and find the 
    first non-zero value.
    """
    #first we are going to define function to help decide thresh off brightness
    brightness = np.log10(np.sum(image)) # in range 5.8-8
    new_max = 350
    new_min = 20
    new_range = new_max - new_min
    old_max = 8
    old_min = 5.7
    old_range = old_max - old_min
    thresh = (((brightness - old_min)*new_range)/old_range) + new_min
    binary = image > thresh
    binary2 = b_e(binary, diamond(1))
    tot = np.sum(binary2)
    if tot < 20:
        top = 1023
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
    """Return 1D array of height of plume in pixels with time.
    
    Uses predefined find_top function on all image arrays in a 3D array.
    """
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
    """Plot the height with revised axis and option to plot smoothed.
    
    Uses calibration image and frame rate to redefine the plot axis
    in terms of cm and seconds.
    
    Keyword arguments:
    height_vals: height of the plume in pixels with time
    raw: plots raw data (default = True)
    raw_col: color of raw data (default = black)
    smooth: plots data smoothed with savgol filter (default = True)
    smooth_col: color of smoothed data (default = red)   
    """
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
    """Convert a 16bit to 8bit image without changing relative brightness
    
    If original image not uint16, print error message.
    """
    if image.dtype == 'uint16':
        import cv2
        im_8 = cv2.convertScaleAbs(image, alpha=255/image.max())
        return im_8
    else:
        print('Image must be in uint16 format')

def remove_back(image, back):
    """Remove the background image of plume.
    
    Keyword arguments:
    image: 1D array containing the image with data
    back: 1D array containing the background of the image.
    """
    removed = image - back
    #make sure it doesn't loop around and get rid of low variation
    removed[(back > image)] = 0
    return removed