# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 01:22:53 2022

@author: david
"""

from skimage import io,color,exposure
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


img=io.imread('../GCD.PNG')[:,:,:3]
gray=color.rgb2gray(img)
gray=exposure.rescale_intensity(gray,in_range=(0,1)
                                         ,out_range='uint8').round().astype('uint8')

def trunc(n,img=gray,plot=False):
    
    
            
    u,s,v=np.linalg.svd(gray,full_matrices=False)
    
    '''
    u=u.round(4)
    s=s.round()
    v=v.round(4)
    '''
    S=s.copy()
    s[n:]=0
    truncated= (u*s)@v 
    truncated=exposure.rescale_intensity(truncated,in_range=(0,255), 
                                         out_range=(0,255)).round().astype('uint8')
    if plot:    
        fig,ax=plt.subplots(1,2,figsize=(10,5))
        ax[0].plot((S)**0.125)
        ax[1].plot(np.cumsum(S)/sum(S))
        ax[0].set_ylabel('(s)**0.125')
        ax[0].set_xlabel('Nº of Singular Values')
        ax[0].set_title('Log of Singular Values')
        ax[1].yaxis.set_major_formatter(PercentFormatter(xmax=1))
        ax[1].set_title('Cummulative Percentage')
        ax[1].set_xlabel('Nº of Singular Values')
    
        fig.tight_layout()
    
        plt.legend()
        plt.show()
        plt.title('Nº de Valores Singulares= %i'%(n))
        plt.imshow(truncated,cmap='gray')
        plt.axis('off')
    
    
    return truncated



