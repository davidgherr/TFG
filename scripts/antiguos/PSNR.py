# -*- coding: utf-8 -*-
"""
Created on Tue May 10 01:26:21 2022

@author: david
"""

from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error as MSE
from SVD_RGB import SVD_RGB
from shuffle import SSVD

img=io.imread('../GCD.PNG')[:,:,:3]

def RMSE(n):
    r=[0,0,0]
    truncated=SVD_RGB(n,img)
    for i in range(3):
        r[i]=MSE(img[:,:,i],truncated[:,:,i])**0.5
        
    
    return np.mean(r)

def PSNR(n,fun=SVD_RGB):
    r=[0,0,0]
    truncated=fun(n,img)  
    for i in range(3):
        r[i]=20*np.log10(255/(MSE(img[:,:,i],truncated[:,:,i]))**0.5)
        
    
    return np.mean(r)
def main():
        
    k=np.linspace(1, 264,264)
    e=[PSNR(int(i),SSVD) for i in k]
    mem=[i*(297+3*264+1)*32/8/1024**2 for i in k]
    
    fig,ax1=plt.subplots()
    color='tab:red'
    ax1.set_xlabel('Número k de valores singulares')
    ax1.set_ylabel('PNSR (dB)',color=color)
    ax1.plot(k,e,color=color)
    ax1.axvline(x=54,linestyle='dotted',color='red',
                alpha=0.5,ymax=0.55)
    ax1.set_ylim(20,80)
    ax1.tick_params(axis='y',labelcolor=color)
    
    ax2=ax1.twinx()
    
    color='tab:blue'
    ax2.set_ylabel('Memoria (MB)',color=color)
    ax2.plot(k,mem,color=color)
    ax2.axhline(y=297*264*24/8/1024**2,linestyle='dotted')
    ax2.tick_params(axis='y',labelcolor=color)
    ax2.set_ylim(0,0.4)
    fig.tight_layout()
    plt.show()
    print(e[54])
if __name__=="__main__":
    main()

