# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:37:20 2022

@author: david
"""


from skimage import io,color,exposure
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


img=io.imread('../GCD.PNG')[:,:,:3]

def SVD_RGB(n,img=img,plot=False):
    
    #la imagen esta en RGB
    
    img=color.rgb2ycbcr(img)
    rows,cols,_=img.shape
    
    
    truncated=img.copy()
    

    Y=img[:,:,0]
    cb=img[:,:,1]
    cr=img[:,:,2]
    
    if rows<=cols:
        A=np.array([Y,cb,cr]).reshape(rows*3,cols)
    else:
        A=np.array([Y,cb,cr]).reshape(rows,cols*3)
        
    u,s,v=np.linalg.svd(A,full_matrices=False)
    
    '''
    
    u=u.round(4)
    s=s.round() 
    v=v.round(4)
    
    '''
    S=s.copy()    
    s[n:]=0
    
    A_r=(u*s)@v
    
    for i in range(3):
        if rows<=cols:
            truncated[:,:,i]=A_r[rows*(i):rows*(i+1),:] 
        else:
            truncated[:,:,i]=A_r[:,cols*(i):cols*(i+1)]
    
    truncated=color.ycbcr2rgb(truncated)
    truncated=exposure.rescale_intensity(truncated,in_range=(0,1)
                                         ,out_range='uint8').round().astype('uint8')
    
    if plot:
        fig,ax=plt.subplots(1,2,figsize=(10,5))
        ax[0].plot(S**0.125)
        ax[1].plot(np.cumsum(S)/sum(S))
        ax[0].set_ylabel('s^0.125')
        ax[0].set_xlabel('Nº of Singular Values')
        ax[0].set_title('eighth root of Singular Values')
        ax[1].yaxis.set_major_formatter(PercentFormatter(xmax=1))
        ax[1].set_title('Cummulative Percentage')
        ax[1].set_xlabel('Nº of Singular Values')
    
        fig.tight_layout()
    
        plt.legend()
        plt.show()
        plt.title('Nº de Valores Singulares= %i'%(n))
        plt.imshow(truncated)
        plt.axis('off')
    
    
    return truncated

