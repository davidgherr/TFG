# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 15:13:06 2022

@author: david
"""

from shuffle import Blocker
from SVD_RGB import SVD_RGB
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from PSNR import PSNR

img=io.imread('../GCD.PNG')[:,:,:3]

def bSVD(n,img=img,rows=12,cols=11,plot=False):
    
    B=Blocker(img,rows,cols)
    i_b=B.toBlocks(img)
    t_b=i_b.copy()
    for i in range(len(i_b)):
        t_b[i]=SVD_RGB(n,i_b[i])
    t=B.fromBlocks(t_b)
    if plot:
        plt.title('Nº de Valores Singulares: %i'%n)
        plt.imshow(t)
        plt.axis('off')
    
    return t
def sim():
    k=np.linspace(1, 33,33)
    e=[PSNR(int(i),bSVD) for i in k]
    mem=[i*(22*3+27+1)*32*132/8/1024**2 for i in k]
    
    fig,ax1=plt.subplots()
    color='tab:red'
    ax1.set_xlabel('Número k de valores singulares')
    ax1.set_ylabel('PNSR (dB)',color=color)
    ax1.plot(k,e,color=color)
    ax1.axvline(x=4,linestyle='dotted',color='red',
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
    print(e[4])