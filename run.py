#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/29/17 7:33 PM 

@author: Hantian Liu
"""
import matplotlib.image as Img
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from carv import carv
import imageio
import scipy.misc
import glob as gb
import cv2

# import source image and resizing
I = np.array(Image.open('1.jpg'))
#I = scipy.misc.imresize(I, [528, 390])
fig1=plt.figure(1)
plt.imshow(I)

# seam carving
nr=20 # rows to remove
nc=15 # columns to remove
[Ic, T, res_list]=carv(I, nr, nc)
#print(T)

# output image after removing (nr) rows and (nc) columns
fig2=plt.figure(2)
plt.imshow(Ic)
plt.show()
fig2.savefig('output.jpg')

# output gif
imageio.mimsave('./output.gif', res_list)