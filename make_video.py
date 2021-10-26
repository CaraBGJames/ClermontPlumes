# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 14:37:39 2021

@author: caraj
"""
img_array = np.load('Experiments/2021-10-21/2021-10-21_exp2_8bit.npy')

mov_name = '21-10-21-exp2.mp4'
fourcc = cv2.VideoWriter_fourcc('H','2','6','4')
fps = 25
size = (1024,512)
out = cv2.VideoWriter(mov_name, -1, fps, size)
frames = img_array_16.shape[2]

for frame in range(100):
    im = mf.to_8bit(img_array_16[:, :, frame])
    out.write(im)
    
out.release