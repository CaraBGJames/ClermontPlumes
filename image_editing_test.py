# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 15:21:41 2021

@author: caraj
"""
# %% Importing and defining functions
import matplotlib.pyplot as plt
import numpy as np
import myfunctions as mf


img_array_2 = np.load('Experiments/2021-10-21/2021-10-21_exp2_16bit_noback.npy')
# %% Finding the plume height
#h_exp1 = mf.plume_height(img_array)
#h_exp2 = mf.plume_height(img_array_2)

mf.plot_height(h_exp1, show = False, col = 'r')
mf.plot_height(h_exp2, show = True, col = 'b')

# %% Plotting

for f in range(400,500):
    show_frame_top(img_array, f)


# %% 

from skimage.filters import try_all_threshold


fig, ax = try_all_threshold(im, figsize=(10, 8), verbose=False)
plt.show()