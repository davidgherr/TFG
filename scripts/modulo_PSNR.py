# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 13:26:01 2022

@author: David Garcerán Herráiz
"""


import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error as MSE


class PSNR:
    '''
    Clase destinada a evaluar el PSNR de cualquier método SVD para 
    distinto número de Valores Singulares.
    '''
    
    def __init__(self, img, fun):
        
        self.RGB = len(img.shape) > 2
        self.img=img
        self.fun=fun(img)
        if hasattr(self.fun,'B'):
            self.max_k=min(self.fun.B.step_m,
                           self.fun.B.step_n)
        else:
            self.max_k=min(img.shape[:2])
        self.mem_lim=img.shape[0]*img.shape[1]/1024
        if self.RGB:
            self.mem_lim*=3/1024
        
        return 
    def RMSE(self,b):
        a=self.img
        if self.RGB:
            r=[0,0,0]
            for i in range(3):
                r[i]=MSE(a[:,:,i],b[:,:,i])**0.5
            r=np.mean(r)
            
        else:
            r=(MSE(a,b))**0.5
        
        return r
    
    def PSNR(self,b):
        a=self.img
        if self.RGB:
            r=[0,0,0]
            for i in range(3):
                r[i]=20*np.log10(255/(MSE(a[:,:,i],b[:,:,i]))**0.5)
            r=np.mean(r)
            
        else:
            r=20*np.log10(255/(MSE(a,b))**0.5)
        
        return r
    
    def sim(self):
        K=np.linspace(1, self.max_k,self.max_k).astype(int)
        e=np.zeros(len(K))
        for n in range(len(K)):
            truncated=self.fun.trunc(int(K[n]))
            e[n-1]=self.PSNR(truncated)
        
        self.mem=np.array([self.fun.mem(int(k)) for k in K]) #en lo que toca
        
        
        corte=np.where(self.mem<=self.mem_lim)[0][-1]
        
        if self.RGB:
            ylim=max(0.4,self.mem_lim)
            unit='MB'
        else:
            ylim=max(120,self.mem_lim)
            unit='KB'
        
        fig,ax1=plt.subplots()
        color='tab:red'
        ax1.set_xlabel('Número k de valores singulares')
        ax1.set_ylabel('PSNR (dB)',color=color)
        ax1.plot(K,e,color=color)
        ax1.axvline(x=corte + 1,linestyle='dotted',color='red',
                    alpha=0.5,ymax=self.mem_lim/ylim)
        ax1.set_ylim(20,80)
        ax1.tick_params(axis='y',labelcolor=color)
        
        ax2=ax1.twinx()
        
        color='tab:blue'
        ax2.set_ylabel('Memoria (%s)'%unit,color=color)
        ax2.plot(K,self.mem,color=color)
        ax2.axhline(y=self.mem_lim,linestyle='dotted')
        ax2.tick_params(axis='y',labelcolor=color)
        ax2.set_ylim(0,ylim)
        fig.tight_layout()
        plt.show()
        print(e[corte])
        
        _=self.fun.plot(int(corte)+1)
        
        return
        
    
    

    