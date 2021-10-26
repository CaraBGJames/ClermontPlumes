# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 15:21:41 2021

@author: caraj
"""
# %% Importing and defining functions
import matplotlib.pyplot as plt
from skimage.exposure import equalize_adapthist
import glob
import numpy as np
import time
import myfunctions as mf
import cv2
# %% Testing image 

im = plt.imread("Experiments/2021-10-15/exp1/exp1001000.tif")
back = plt.imread("Experiments/2021-10-15/background1/background1000010.tif")
print('in data type:',im.dtype)

test = mf.remove_back(im,back)
test2 = equalize_adapthist(test)

mf.show_im(test, 'Greys_r')
mf.show_im(test2, 'Greys_r')

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
    img_noback = mf.remove_back(img, back_av)
    img_array[:, :, count] = img_noback
    count += 1
    if count%100 == 0:
        print(count)

t1 = time.time()
print(t1-t0)


# %% change to 8bit
img_array_8 = np.zeros((512,1024,4823), dtype = 'uint8')
count = 0
for f in range(img_array_16.shape[2]):
    f_16 = img_array_16[:,:,f]
    f_8 = cv2.convertScaleAbs(f_16, alpha=255/f_16.max())
    img_array_8[:, :, f] = f_8
    if count % 100 == 0:
        print(count)
    count+=1
# %% Save the image array

np.save('Experiments/2021-10-21_exp1_8bit',img_array_8)
    
# %% Load the image array

img_array = np.load('Experiments/2021-10-21/2021-10-21_exp1_16bit.npy')

# %% Finding the plume height

height_arr = []
count = 0
for n in range(img_array.shape[2]):
    h = mf.find_top(img_array[:,:,n], 30)
    height_arr.append(h)
    if count % 100 == 0:
        print(count)
    count+=1

# %% Make video
mov_name = '21-10-21-exp1.mp4'
fourcc = cv2.VideoWriter_fourcc('H','2','6','4')
fps = 25
size = (1024,512)
out = cv2.VideoWriter(mov_name, -1, fps, size)
frames = img_array_16.shape[2]

for frame in range(100):
    im = mf.to_8bit(img_array_16[:, :, frame])
    out.write(im)
    
out.release

# %% Filtering

from scipy.signal import lfilter

n = 100  # the larger n is, the smoother curve will be
b = [1.0 / n] * n
a = 1
yy = lfilter(b, a, height_arr_150)
plt.plot(yy, linewidth=2, linestyle="-", c="b")  # smooth by filter

# %% calibration

height = np.concatenate((np.zeros(13), np.linspace(0,76,1024-13)))
