# -*- coding: utf-8 -*-
"""
Created on Mon May 30 16:48:12 2022

@author: david
"""

from skimage import io,color,exposure
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error as MSE
from SVD import trunc

img=io.imread('../GCD.PNG')[:,:,:3]
gray=color.rgb2gray(img)
gray=exposure.rescale_intensity(gray,in_range=(0,1)
                                         ,out_range='uint8').round().astype('uint8')


def PSNR(a,b=None,svd=None):
    if svd:
        b=trunc(svd,gray)
    r=20*np.log10(255/(MSE(a,b))**0.5)
        
    
    return r

def main():

    k=np.linspace(1, 264,264)
    e=[PSNR(gray,svd=int(i)) for i in k]
    mem=[i*(297+264+1)*32/8/1024 for i in k]
    
    fig,ax1=plt.subplots()
    color='tab:red'
    ax1.set_xlabel('Número k de valores singulares')
    ax1.set_ylabel('PNSR (dB)',color=color)
    ax1.plot(k,e,color=color)
    ax1.axvline(x=35,linestyle='dotted',color='red',
                alpha=0.5,ymax=0.65)
    ax1.set_ylim(20,80)
    ax1.tick_params(axis='y',labelcolor=color)
    
    ax2=ax1.twinx()
    
    color='tab:blue'
    ax2.set_ylabel('Memoria (KB)',color=color)
    ax2.plot(k,mem,color=color)
    ax2.axhline(y=297*264/1024,linestyle='dotted')
    ax2.tick_params(axis='y',labelcolor=color)
    ax2.set_ylim(0,120)
    fig.tight_layout()
    plt.show()

if __name__=="__main__":
    main()

