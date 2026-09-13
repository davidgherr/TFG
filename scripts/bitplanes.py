# -*- coding: utf-8 -*-
"""
Created on Wed May 11 18:56:38 2022

@author: david
"""

from skimage import io,color
import numpy as np
import matplotlib.pyplot as plt
import pywt

img=io.imread('../GCD.PNG')[:,:,:3]
#g=color.rgb2gray(img)
g=img[:,:,0]
binary=[]
for i in range(g.shape[0]):
    for j in range(g.shape[1]):
        binary.append(np.binary_repr(g[i][j],width=8))
 
#Extract the bit planes


planes=[]
for b in range(8):
    planes.append((np.array([int(i[b]) for i in binary] , dtype=np.uint8)*(2**(7-b))).reshape(img.shape[0],img.shape[1])
)
    
for b in range(8):
    plt.imshow(planes[b],cmap='gray')
    plt.show()

new=planes[0]+planes[1]+planes[2]+planes[3]+planes[4]


