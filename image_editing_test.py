# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 15:21:41 2021

@author: caraj
"""
# %% Importing and defining functions
import matplotlib.pyplot as plt
import numpy as np
import myfunctions as mf


img_array = np.load('Experiments/2021-10-21/2021-10-21_exp1_16bit.npy')
# %% Finding the plume height

h_exp1 = mf.plume_height(img_array)

#name = '2021-10-21_exp3_height'
#np.save(directory+name,h_exp1)

# %% Plotting

mf.plot_height(h_exp1, smooth = False)


# %% 
import matplotlib
import matplotlib.pyplot as plt


from skimage.filters import try_all_threshold


fig, ax = try_all_threshold(im, figsize=(10, 8), verbose=False)
plt.show()