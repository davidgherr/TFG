# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 18:06:30 2022

@author: David Garcerán Herráiz
"""

import numpy as np
import pandas as pd
from skimage import io,color
from modulo_SVD import SVD_raw,rescale
from modulo_PSNR import PSNR

class shuffler:
    '''
    Permuta los componentes de un vector, guardando la trasformación 
    para poder la inversa.
    '''
    def __init__(self,n):
        self.dir=pd.DataFrame({'A':np.array(range(n)),
                               'B':np.random.permutation(range(n))})
    
    def shuffle(self,A):
        A=np.array(A)
        return A[self.dir['B']]
    
    def inverse(self,B):
        B=np.array(B)
        INV=self.dir.sort_values(by='B')
        return B[INV['A']]
    
class Blocker:
    """
    Divide y reconstruye una imagen en bloques, el número de bloques por
    dimensión será el divisor más cercano a la raiz de dicha dimensión.
    """
    def __init__(self,X):
        nd=self.NearestDiv(X)
        self.a=nd[0]
        self.b=nd[1]
        self.shape=X.shape
    
    def NearestDiv(self,X):
        nd=list()
        for d in X.shape[:2]:
            divs=np.array([i for i in range(1,d+1) if d % i==0])
            idx=np.argmin(np.abs(divs-d**0.5))
            nd.append(divs[idx])
        return nd
        
    def toBlocks(self,X):
        m,n=X.shape[:2]
        self.step_m=m//self.a
        self.step_n=n//self.b
        chain=list()
        for i in range(0,m,self.step_m):
            for j in range(0,n,self.step_n):            
                chain.append(X[i:(i+self.step_m), j:(j+self.step_n)])
        return chain
    
    def fromBlocks(self,chain):
        A=np.zeros(self.shape,dtype='uint8')
        idx=list()
        for i in range(0,self.shape[0],self.step_m):
            for j in range(0,self.shape[1],self.step_n):
                idx.append((i,j))
        
        for n,d in enumerate(idx):
            i,j=d
            
            A[i:(i+self.step_m),j:(j+self.step_n)]=chain[n]
        
        return A

class SSVD(SVD_raw):
    """
    Método en el que se permutan los bloques de la imagen y se ejecuta la 
    SVD
    """
    def __init__(self,img):
        
        self.B=Blocker(img)
        blocks=self.B.toBlocks(img)
        self.SH=shuffler(len(blocks))
        blocks_S=self.SH.shuffle(blocks)
        img_S=self.B.fromBlocks(blocks_S)
        
        SVD_raw.__init__(self,img_S)
    
    def trunc(self,k):
        
        truncated=SVD_raw.trunc(self,k)
        blocks_S=self.B.toBlocks(truncated)
        blocks=self.SH.inverse(blocks_S)
        img_r=self.B.fromBlocks(blocks)
        
        return img_r
        
        
def main():
    #RGB
    img=img=io.imread('../GCD.PNG')[:,:,:3]
    A=PSNR(img,SSVD)
    A.sim()
    
    #gray
    gray=color.rgb2gray(img)
    gray=rescale(gray,(0,1))
    A=PSNR(gray,SVD_raw)
    A.sim()
    
    

if __name__=="__main__":
    main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        