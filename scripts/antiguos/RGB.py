# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 00:08:44 2022

@author: david
"""

from skimage import io,color
import numpy as np
import matplotlib.pyplot as plt

img=io.imread('../GCD.PNG')[:,:,:3]
A=color.rgb2ycbcr(img)

Y=A[:,:,0]
Cb=A[:,:,1]
Cr=A[:,:,2]

fig,ax=plt.subplots(1,3,sharey=True)
ax[0].imshow(Y,cmap='gray')
ax[0].set_title('Y')
ax[0].set_axis_off()
ax[1].imshow(Cb,cmap='gray')
ax[1].set_title('Cb')
ax[1].set_axis_off()
ax[2].imshow(Cr,cmap='gray')
ax[2].set_title('Cr')
ax[2].set_axis_off()
plt.show()




