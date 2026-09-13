# -*- coding: utf-8 -*-
"""
Created on Sat May 14 13:50:42 2022

@author: David Garcerán Herráiz
"""

from WDR import encode_WDR,decode_WDR,DWT, inverseDWT
from HUFFMAN import HUFF
from SVD import trunc
from PSNR_gray import PSNR
from skimage import io,color,exposure
import bitstring
import matplotlib.pyplot as plt

img=io.imread('../GCD.PNG')[:,:,:3]
g=color.rgb2gray(img)
g=exposure.rescale_intensity(g,in_range=(0,1)
                                         ,out_range='uint8').round().astype('uint8')
g_t=trunc(150,g)
coefs,slices,shapes=DWT(g_t,2,'db1')
iniT, bitstream =encode_WDR(coefs,12,2)

H=HUFF(bitstream)
e=H.encode(bitstream)

f=open('prueba.bin','wb')
e.tofile(f)
f.close()
#12.2 KB

d=bitstring.BitArray(filename='./prueba.bin')
bit=H.decode(d)
array=decode_WDR(iniT,bit,slices)
I=inverseDWT(array,slices,shapes)
plt.imshow(I,cmap='gray')
plt.title(PSNR(g,I[:,:297]))
