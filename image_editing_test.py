# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 15:21:41 2021

@author: caraj
"""
# %% Importing and defining functions
import matplotlib.pyplot as plt
from skimage.transform import rotate
from skimage.exposure import equalize_adapthist
import glob
import numpy as np
import time


def show_im(image, cmap_type = 'viridis', title=''):
    """shows image as plot"""
    im = rotate(image,-90, resize = True)
    plt.imshow(im, cmap = cmap_type)
    plt.title(title)
    plt.axis('off')
    plt.show()
    
def hist_im(image, nbins = 256):
    """Plot a histogram of the pixel variation in image"""
    plt.hist(image.ravel(),bins = nbins)
    
def to_8bit(image, show = True):
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

def find_top(image, thresh = 400):
    """Find the top of the plume image"""
    binary = image > thresh
    top = np.where(sum(binary) > 0)[0][0]
    return top
  
# %% Testing image 

im = plt.imread("Experiments/2021-10-15/exp1/exp1001000.tif")
back = plt.imread("Experiments/2021-10-15/background1/background1000010.tif")
print('in data type:',im.dtype)

test = remove_back(im,back)
test2 = equalize_adapthist(test)

show_im(test, 'Greys_r')
show_im(test2, 'Greys_r')

#%% Get average background to remove

back_files = glob.glob('Experiments/2021-10-21/back1/*.tif')
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

filenames = glob.glob('Experiments/2021-10-21/exp1/*.tif')
file1 = plt.imread(filenames[0])
height, width = file1.shape
img_array = np.zeros((height, width, len(filenames)), dtype = 'uint16')
count = 0
for file in filenames:
    img = plt.imread(file)
    img_noback = remove_back(img, back_av)
    img_array[:, :, count] = img_noback
    count += 1
    if count%100 == 0:
        print(count)

t1 = time.time()
print(t1-t0)

# %% Save the image array

np.save('2021-10-21_exp1',img_array)
    

