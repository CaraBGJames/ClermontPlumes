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

im = plt.imread("2021-10-15/exp1/exp1001000.tif")
back = plt.imread("2021-10-15/background1/background1000010.tif")
print('in data type:',im.dtype)

test = remove_back(im,back)
test2 = equalize_adapthist(test)

show_im(test, 'Greys_r')
show_im(test2, 'Greys_r')

# %% Finding height variation

img_array = []
for filename in glob.glob('C:/New folder/Images/*.jpg'):
how    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
