# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 15:21:41 2021

@author: caraj
"""
# %% Importing and defining functions
import matplotlib.pyplot as plt
import numpy as np
import myfunctions as mf
from skimage.transform import rotate
# %% Read in data
img_array = np.load('Experiments/2021-11-02/2021-11-02_exp2_16bit_noback.npy')
#img_array_2 = np.load('Experiments/2021-10-21/2021-10-21_exp2_16bit_noback.npy')
#img_array_3 = np.load('Experiments/2021-10-21/2021-10-21_exp3_16bit.npy')
#img_array_4 = np.load('Experiments/2021-10-15/2021-10-15_exp1_16bit_noback.npy')

#h_exp1 = np.load('Experiments/Heights/2021-10-21_exp1.npy')
#h_exp2 = np.load('Experiments/Heights/2021-10-21_exp2.npy')
#h_exp3 = np.load('Experiments/Heights/2021-10-21_exp3.npy')
#h_exp4 = np.load('Experiments/Heights/2021-10-15_exp1.npy')
# %% Plotting
to_plot= [h_exp1/0.62, h_exp2/0.62, h_exp3/0.66, h_exp4/0.41]
labels = ['exp1','exp2','exp3','exp4']
col = ['r','b','g','k']

for n in range(len(to_plot)):
    mf.plot_height(to_plot[n], raw = False, smooth_col = col[n])
plt.legend(labels)
plt.show()

# %% 
n = 2200
dif = 100
image = mf.remove_back(img_array[:,:,n],img_array[:,:,n-dif])

for i in range(2000, 5400, 10):
    #image = mf.remove_back(img_array[:,:,i],img_array[:,:,i-5])
    image = img_array[:,:,i]
    im = rotate(image,-90, resize = True)
    plt.imshow(im, cmap = 'Greys_r')
    plt.axis('off')
    #plt.colorbar()
    plt.show()