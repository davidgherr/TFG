# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:16:42 2022

@author: david
"""

from PSNR import RMSE
from SVD_RGB import SVD_RGB
import numpy as np
from scipy.optimize import minimize

#Parece que a partir de 35dB (mas o menos) se aprecia 

def RELU(k):
    L=0.75*264*297/(3*264+297+1)
    
    if k>L:
        r=45*k
    else:
        r=0.25*k
    return r

def objective(k):
    K=int(k[0])
    
    return RELU(K) + 1.25*RMSE(K)



k0=[50,1]
objective(k0)
b=(0.0,264.0)
bounds=(b,b)

sol=minimize(objective, k0,method='Powell',
             bounds=bounds)

K=int(sol.x[0])
SVD_RGB(K,plot=True)


