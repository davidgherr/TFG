# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 20:37:15 2022

@author: David Garcerán Herráiz
"""

from modulo_PSNR import PSNR
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

class OPT_K(PSNR):
    '''
    Clase pensada para optimizar k de forma no lineal, para cualquier imagen
    y variante SVD.
    '''
    def __init__(self,img,fun,difk=False):
        """
        

        Parameters
        ----------
        img : np.array
            Imagen objeto.
        fun : class
            Variante de SVD.
        difk : bool, optional
            Asumir o no la misma k para las variantes
            por bloques. The default is False.

        Returns
        -------
        None.

        """
        PSNR.__init__(self,img,fun)
        if hasattr(self.fun,'B') and difk:
            n=self.fun.B.a*self.fun.B.b
        else:
            n=2
        
        self.k0=np.repeat(self.max_k//4-2,n)
        bound=(1,self.max_k)
        self.bounds=tuple([bound for i in range(n)])

        
    
    
    def RELU_mem(self,k):
        
        if self.fun.mem(k)>self.mem_lim:
            r=45e5*self.fun.mem(k)
        else:
            r=self.fun.mem(k)/self.mem_lim
        return r
    
    def RELU_e(self,k):
        e=self.PSNR(self.fun.trunc(k))
        ma=50
        if e<36:
            r=5e4 - e
        elif e<=ma:
            r=ma/(ma-36)-e/(ma-36)
        else:
            r=0
        return r   
    
    def f_obj(self,k):
        if len(k)==2:
            K=int(k[0])
        else:
            K=np.array([int(i) for i in k])
        
        return (self.RELU_mem(K)**2 - self.RELU_e(K)**2)**0.5
    
    def callback(self,X):
        print([i for  i in X])
        if len(X)==2:
            
            self.fun.plot(X[0])
        else:
            self.fun.plot(X)
        plt.plot()
    
    def exe(self,m='Powell',it=5):

        sol=minimize(self.f_obj,
                     self.k0,
                     method=m,
                     bounds=self.bounds,
                     options={'maxiter':it,'disp':True})
        K=[int(k) for k in sol.x]
        if len(K)==2:
            self.fun.plot(int(K[0]))
            plt.show()
            print('Tasa de compresión: {0:.2%}'.format((1-self.RELU_mem(K[0]))))
            print('PSNR: %0.2f dB'%self.PSNR(self.fun.trunc(int(K[0]))))
        else:
            self.fun.plot(K)
            plt.show()
            print('Tasa de compresión: {0:.2%}'.format(1-self.RELU_mem(K)))
            print('PSNR: %0.2f dB'%self.PSNR(self.fun.trunc(K)))
        return 
    

    
    
    
            
        
