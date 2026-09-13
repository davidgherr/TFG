# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 22:02:37 2022

@author: david
"""

from modulo_SVD import SVD_raw,rescale
from modulo_SVD_bloques import SVD_bloques
from modulo_aprox import RAW_approx, Bloques_aprox
from modulo_minimize import OPT_K
from skimage import io,color

img1=io.imread('../tests/radio.jpg')
img1=rescale(color.rgb2gray(img1),in_range=(0,1))


A=OPT_K(img1,SVD_raw)
A.exe()
A=OPT_K(img1,SVD_bloques)
A.exe()
A=OPT_K(img1,RAW_approx)
A.exe()
A=OPT_K(img1,Bloques_aprox)
A.exe()