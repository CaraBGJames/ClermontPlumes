# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 15:21:41 2021

@author: caraj
"""
# %% Importing and defining functions
import matplotlib.pyplot as plt
import numpy as np
import myfunctions as mf

# %% Read in data
#img_array_1 = np.load('Experiments/2021-10-21/2021-10-21_exp1_16bit.npy')
#img_array_2 = np.load('Experiments/2021-10-21/2021-10-21_exp2_16bit_noback.npy')
#img_array_3 = np.load('Experiments/2021-10-21/2021-10-21_exp3_16bit.npy')
img_array_4 = np.load('Experiments/2021-10-15/2021-10-15_exp1_16bit_noback.npy')

#h_exp1 = np.load('Experiments/Heights/2021-10-21_exp1.npy')
#h_exp2 = np.load('Experiments/Heights/2021-10-21_exp2.npy')
#h_exp3 = np.load('Experiments/Heights/2021-10-21_exp3.npy')

# %% Plotting
h_exp4 = mf.plume_height(img_array_4)

# %% 

from skimage.filters import try_all_threshold


fig, ax = try_all_threshold(im, figsize=(10, 8), verbose=False)
plt.show()