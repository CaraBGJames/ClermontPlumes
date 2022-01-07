# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 18:18:58 2022

@author: caraj
"""

#%% Little guide for Amelie to understand my code :

#Importing (you need to have the height_find.py file in the same directory)
from height_find import height_find
from height_find import plume_find
import matplotlib.pyplot as plt
from skimage.transform import rotate
import glob

#First set it up so if your files are in sequential order you can access them
#e.g. if your images are in a folder called AmeliesExp and named 'exp100001' to
#'exp101000' you would put...
directory = 'AmeliesExp'
exp_n = '1'
t = 650 #just an example frame
dt = 50 

#This will allow you to loop through file names easily by changing the above
#numbers, e.g. (print to see)
I_t_name = directory+'/exp'+exp_n+str(t).zfill(4)+'.tif'

#So actually calling the files:
I_t =  plt.imread(directory+'/exp'+exp_n+str(t).zfill(4)+'.tif')
I_step = plt.imread(directory+'/exp'+exp_n+str(t+dt).zfill(4)+'.tif')
I_ref = plt.imread(directory+'/exp'+exp_n+'00001.tif') #first frame

#and then put these into predefined functions to see if it works!
h = height_find(I_t, I_step, I_ref)
outline = plume_find(I_t, I_step, I_ref)

#%% Seeing the plume height (this is from my code so names probs wrong and 
#there are also some extra folders in there I think)

#define directory and experiment number
directory = 'Experiments/2021-11-29'
exp_n = '1'

#Define the background image (here first image)
I_ref = plt.imread(directory+'/back'+exp_n+'/back'+exp_n+'000001.tif')

#get a list of all the file names in your folder
filenames = glob.glob(directory+'/exp'+exp_n+'/exp'+exp_n+'*.tif') 
n = len(filenames)
#decide your dt, have a play see what works best!
dt = 10

#make empty arrays for height and time results
T = list(range(1, n-dt, 10))
H = np.zeros(len(T))

#loop through the images
count = 0
for t in T:
    #read in the images
    I_t =  plt.imread(
        directory+'/exp'+exp_n+'/exp'+exp_n+str(t).zfill(6)+'.tif')
    I_step = plt.imread(
        directory+'/exp'+exp_n+'/exp'+exp_n+str(t+dt).zfill(6)+'.tif')
    
    #find height using defined function then save to the arrays
    h = height_find(I_t, I_step, I_ref)
    H[count] = h
    count +=1
    p = count/len(T)*100
    if count%20==0:
        print(p)
        im2 = rotate(I_t,-90, resize = True)
        plt.figure(figsize = (18,18))
        plt.imshow(im2, cmap = 'Greys_r', vmin = 0, vmax = 0.005)
        plt.axhline((1024-h), color = 'w', linewidth = 1)
        plt.axis('off')
        plt.show()
        
#plot out graph
plt.plot(T,H)
