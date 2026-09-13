# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 20:18:37 2022

@author: david
"""


import numpy as np
import pandas as pd
from skimage import io

class shuffler:
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
    def __init__(self,X,rows=6,cols=9):
        self.rows=rows
        self.cols=cols
        self.shape=X.shape
        
    def toBlocks(self,X):
        m,n,_=X.shape
        self.step_m=m//self.rows
        self.step_n=n//self.cols
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
            
        
    
    
    
img=io.imread('../GCD.PNG')[:,:,:3]

def SSVD(n,img=img):
    
    B=Blocker(img)
    blocks=B.toBlocks(img)
    S=shuffler(len(blocks))
    blocks_S=S.shuffle(blocks)
    img_S=B.fromBlocks(blocks_S)
    
    #SVD
    truncated=SVD_RGB(n,img_S)
    blocks_S=B.toBlocks(truncated)
    blocks=S.inverse(blocks_S)
    img_r=B.fromBlocks(blocks)

    
    
    
    return img_r



