# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 19:27:35 2022

@author: David Garcerán Herráiz
"""
from modulo_SVD import SVD_raw,rescale
from skimage import io,color
from modulo_PSNR import PSNR
from modulo_SVD_bloques import SVD_bloques
import numpy as np

class RAW_approx(SVD_raw):
    """
    Mismo procedimiento que SVD normal, sólo que se redondean los valores
    de las matrices de la factorización.
    """
    def __init__(self,img):
        SVD_raw.__init__(self,img)
        self.u=self.u.round(4)
        self.v=self.v.round(4)
        self.s=self.s.round()
    
    def mem(self,k):
        
        if self.RGB:
            rows,cols,_=self.img.shape
            
            m= k*(max(rows,cols)+3*min(rows,cols)+2)*16/8/1024**2 #MB
        else:
            rows,cols=self.img.shape
            m=k*(rows+cols+2)*16/8/1024 #KB
       
        return  m
    
class Bloques_aprox(SVD_bloques):
    """
    Mismo procedimiento que SVD en bloques, sólo que se redondean los valores
    de las matrices de la factorización.
    """
    def __init__(self,img):
        SVD_bloques.__init__(self,img)
    
    def trunc(self,k):
        #Si sólo hay una entrada, asumimos que es la misma para todos
        if type(k) == int:
            K=np.repeat(k,self.B.a*self.B.b)
        # De lo contrario, habrá que tener una por cada bloque.
        else:
            K=k
        
        t_b=self.i_b.copy()
        t_b=self.i_b.copy()
        matrices=list()
        for i in range(len(t_b)):
            FACT=SVD_raw(self.i_b[i])
            FACT.u=FACT.u.round(4)
            FACT.v=FACT.v.round(4)
            FACT.s=FACT.s.round()
            t_b[i]=FACT.trunc(int(K[i]))
            matrices.append((FACT.u[:,:int(K[i])],
                             FACT.s[:int(K[i])],
                             FACT.v[:int(K[i]),:]))
        truncated=self.B.fromBlocks(t_b)
        return truncated
    
    def mem(self,k):
        a=self.B.a
        b=self.B.b
        
        if type(k) == int:
            K=np.repeat(k,a*b)
        else:
            K=k
        
        if self.RGB:
            rows,cols,_=self.img.shape
            
            m= sum(K)*16*(max(rows/a,cols/b)+3*min(rows/a,cols/b)+2)/8/1024**2#MB
        else:
            rows,cols=self.img.shape
            m=sum(K)*(rows/a+cols/b+2)*16/8/1024 #KB
       
        return  m

def main():
    #RGB
    img=io.imread('../GCD.PNG')[:,:,:3]
    #A=PSNR(img,RAW_approx)
    A=PSNR(img,Bloques_aprox)
    A.max_k=min(A.fun.B.step_m,
                A.fun.B.step_n)
    A.sim()
    
    #gray
    gray=color.rgb2gray(img)
    gray=rescale(gray,(0,1))
    #A=PSNR(gray,RAW_approx)
    A=PSNR(gray,Bloques_aprox)
    A.max_k=min(A.fun.B.step_m,
                A.fun.B.step_n)
    A.sim()

if __name__=="__main__":
    main()