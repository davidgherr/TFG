# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 17:45:29 2022

@author: David Garcerán Herráiz
"""

from modulo_shuffled import Blocker
from modulo_SVD import SVD_raw,rescale
import numpy as np
import matplotlib.pyplot as plt
from modulo_PSNR import PSNR
from skimage import io,color

class SVD_bloques():
    """
    Divide la imagen en bloques y aplica la SVD a cada bloque.
    """
    def __init__(self,img):
        self.RGB=len(img.shape)>2
        self.img=img
        self.B=Blocker(img)
        self.i_b=self.B.toBlocks(img)
        
    def trunc(self,k):
        #Si sólo hay una entrada, asumimos que es la misma para todos
        if type(k) == int:
            K=np.repeat(k,self.B.a*self.B.b)
        # De lo contrario, habrá que tener una por cada bloque.
        else:
            K=k
        
        t_b=self.i_b.copy()
        matrices=list()
        for i in range(len(t_b)):
            FACT=SVD_raw(self.i_b[i])
            t_b[i]=FACT.trunc(int(K[i]))
            matrices.append((FACT.u[:,:int(K[i])],
                             FACT.s[:int(K[i])],
                             FACT.v[:int(K[i]),:]))
        truncated=self.B.fromBlocks(t_b)
        return truncated
    
    def plot(self,k):
        if type(k) == int:
            plt.title('Nº de Valores Singulares= %i'%(k))
        else:
            plt.title('Nº de Valores Singulares variable')
        if self.RGB:
            plt.imshow(self.trunc(k))
        else:
            plt.imshow(self.trunc(k),cmap='gray')
        plt.axis('off')
        
    def mem(self,k):
        a=self.B.a
        b=self.B.b
        if type(k) == int:
            K=np.repeat(k,a*b)
        else:
            K=k
        
        if self.RGB:
            rows,cols,_=self.img.shape
            
            m= np.sum(K)*32*(max(rows/a,cols/b)+3*min(rows/a,cols/b)+1)/8/1024**2#MB
        else:
            rows,cols=self.img.shape
            m=np.sum(K)*(rows/a+cols/b+1)*32/8/1024 #KB
       
        return  m
    

def main():
    #RGB
    img=img=io.imread('../GCD.PNG')[:,:,:3]
    A=PSNR(img,SVD_bloques)
    A.max_k=min(A.fun.B.step_m,
                A.fun.B.step_n)
    
    A.sim()
    
    #gray
    gray=color.rgb2gray(img)
    gray=rescale(gray,(0,1))
    A=PSNR(gray,SVD_bloques)
    A.max_k=min(A.fun.B.step_m,
                A.fun.B.step_n)
    A.sim()
    
    
if __name__=="__main__":
    main()
    
    