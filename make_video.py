# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 14:04:14 2021

@author: caraj
"""
import time
start = time.time()

import cv2
from skimage import io
from skimage import util
import numpy as np
import glob
 
#make list of all the image files, put them into an array to write vid from
#here you could do any editing you fancy too
img_array = []
count = 0
for filename in glob.glob('2021-11-15/exp1/*.tif'):
    while count < 120:
        img = io.imread(filename)
        img_8 = util.img_as_ubyte(img)
        height, width = img_8.shape
        size = (width,height)
        img_array.append(img_8)
        count += 1
 
#variations for writing video
vid_name = 'test_vid.avi'
fourcc = 
fps = 120

out = cv2.VideoWriter(vid_name, cv2.VideoWriter_fourcc(fourcc), fps, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

end = time.time()
print(end - start)