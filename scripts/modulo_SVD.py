# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:15:41 2022

@author: David Garcerán Herráíz
"""

from skimage import io,color,exposure
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from modulo_PSNR import PSNR
import warnings
warnings.filterwarnings("ignore")

def rescale(img,in_range,out_range=(0,255)):
    '''
    Parameters
    ----------
    img : np.array
        imagen a escalar
    in_range : tupla
        rango de valores en los que esta img
    out_range : tupla, optional
        rango de valores de salida. The default is (0,255).

    Returns
    -------
    Escala los valores de la imagen a de un rango a otro.

    '''
    
    return exposure.rescale_intensity(img,in_range=in_range
                                         ,out_range=out_range).round().astype('uint8')


class SVD_raw:
    """
    Clase destinada a ejecutar la SVD normal sobre cualquier imagen
    """
    
    def __init__(self,img):
        self.RGB= len(img.shape)>2
        self.img=img
        if self.RGB:
            img=color.rgb2ycbcr(img)
            rows,cols,_=img.shape
            Y=img[:,:,0]
            cb=img[:,:,1]
            cr=img[:,:,2]
            
            if rows<=cols:
                A=np.array([Y,cb,cr]).reshape(rows*3,cols)
            else:
                A=np.array([Y,cb,cr]).reshape(rows,cols*3)
            
            self.u,self.s,self.v=np.linalg.svd(A,full_matrices=False)
        
        else:
            self.u,self.s,self.v=np.linalg.svd(self.img,full_matrices=False)
        
        self.S=self.s.copy()
        
        return
    def trunc(self,k):
        """
        Parameters
        ----------
        k : int
            Número de valores singulares.

        Returns
        -------
        truncated : np.array
            Imagen reconstruida con esos valores singulares.

        """
        u=self.u[:,:k]
        s=self.s[:k]
        v=self.v[:k,:]
        A= (u*s)@v
        
        if self.RGB:
            
            rows,cols,_=self.img.shape
            truncated=np.zeros((rows,cols,3))
            for i in range(3):
                if rows<=cols:
                    truncated[:,:,i]=A[rows*(i):rows*(i+1),:] 
                else:
                    truncated[:,:,i]=A[:,cols*(i):cols*(i+1)]
            truncated=color.ycbcr2rgb(truncated)
            truncated=exposure.rescale_intensity(truncated,in_range=(0,1)
                                         ,out_range='uint8').round().astype('uint8')
        else:
            truncated=rescale(A,(0,255))
        
        return truncated
    
    def plot(self,k):
        """
        Muestra la imagen reconstruida con k valores singulares

        Parameters
        ----------
        k : int
            Número de valores singulares.

        Returns
        -------
        None.

        """
        fig,ax=plt.subplots(1,2,figsize=(10,5))
        ax[0].plot(self.S**0.125)
        ax[1].plot(np.cumsum(self.S)/sum(self.S))
        ax[0].set_ylabel('s^0.125')
        ax[0].set_xlabel('Nº of Singular Values')
        ax[0].set_title('eighth root of Singular Values')
        ax[1].yaxis.set_major_formatter(PercentFormatter(xmax=1))
        ax[1].set_title('Cummulative Percentage')
        ax[1].set_xlabel('Nº of Singular Values')
    
        fig.tight_layout()
    
        plt.legend()
        plt.show()
        plt.title('Nº de Valores Singulares= %i'%(k))
        if self.RGB:
            plt.imshow(self.trunc(k))
        else:
            plt.imshow(self.trunc(k),cmap='gray')
        plt.axis('off')
    
    def mem(self,k):
        """
        Calcula la memoria que ocuparía la reconstrucción

        Parameters
        ----------
        k : int
            Número de Valores Singulares.

        Returns
        -------
        m : float
            Memoria usada, MB si es a color, KB si no.

        """
        
        if self.RGB:
            rows,cols,_=self.img.shape
            
            m= k*(max(rows,cols)+3*min(rows,cols)+1)*32/8/1024**2 #MB
        else:
            rows,cols=self.img.shape
            m=k*(rows+cols+1)*32/8/1024 #Kb
       
        return  m
        
def main():
    #RGB
    img=img=io.imread('../GCD.PNG')[:,:,:3]
    A=PSNR(img,SVD_raw)
    A.sim()
    
    #gray
    gray=color.rgb2gray(img)
    gray=rescale(gray,(0,1))
    A=PSNR(gray,SVD_raw)
    A.sim()
    
    

if __name__=="__main__":
    main()