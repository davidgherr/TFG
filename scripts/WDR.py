# -*- coding: utf-8 -*-
"""
Created on Thu May 12 20:36:04 2022

@author: David Garcerán Herráiz
"""

from skimage import io,color,exposure
import numpy as np
import matplotlib.pyplot as plt
import pywt
import re
from SVD import trunc

img=io.imread('../GCD.PNG')[:,:,:3]
g=color.rgb2gray(img)
g=exposure.rescale_intensity(g,in_range=(0,1)
                                         ,out_range='uint8').round().astype('uint8')

def DWT(g,n=4,w='db1'):
    coeffs=pywt.wavedec2(g,w,level=n)
    #coeff_arr,coeff_slices=pywt.coeffs_to_array(coeffs)
    coeff_arr,coeff_slices,coeff_shape=pywt.ravel_coeffs(coeffs)
    
    return coeff_arr,coeff_slices,coeff_shape

def inverseDWT(coef_arr,coeff_slices,coeff_shapes,w='db1'):
    #coeffs_filt=pywt.array_to_coeffs(coef_arr, coeff_slices,output_format='wavedec2')
    coeffs_filt=pywt.unravel_coeffs(coef_arr, coeff_slices, coeff_shapes,
                                    output_format='wavedec2')
    Arecon=pywt.waverec2(coeffs_filt,wavelet=w)
    
    return Arecon


def bit_plane(arr,idx):
    '''
    Indices codificados empezando en 1 OJO
    '''
    
    dif=idx.copy()+1
    dif[1:]=np.diff(idx+1)
    
    binary=[format(i,'b') for i in dif]
    
    msb=[b[0] for b in binary]
    
    if all([i =='1' for i in msb]):
        binary=[b[1:] for b in binary]
    
    results=''
    for i in range(len(arr)):
        if arr[i] >=0:
            results+='+'
        else:
            results+='-'
        results+=binary[i]
    return results


def new_bit(i,T):
    li=T
    hi=2*T
    f=(hi-li)/2+li
    if np.abs(i)>=f:
        new='1'
    else:
        new='0'
    return new

def encode_WDR(coefs,loops=12,conv=2):
    
    
    #Initial stage
    T=np.max(coefs)*conv
    iniT=np.max(coefs)*conv
    
    SCS='' # significative
    TPS=np.array([]) # temporaly significative
    ICS=coefs.copy() # not significative
    
    
    #loop
    for times in range(loops):
        
        T/=conv
    
        #Significant pass stage
          
        idx=np.where(np.abs(ICS)>=T)
        values=ICS[idx]
        TPS=np.append(TPS,values)
        ICS=np.delete(ICS,idx)
        
        cod=bit_plane(values, idx[0])
        
        #refining stage
        splitted=re.split('(\W\d*)',cod)
        splitted=[s for s in splitted if s!='']
        
        new=''
        
        for i,c in enumerate(TPS):
            subcod=splitted[i]
            new+=subcod[0]+new_bit(c,T)+subcod[1:]
                
        
        SCS+=new + '|'
        
        TPS=np.array([])
    
    
            
    return (int(iniT),SCS)


def PAD(a,b):
    r=a.copy()
    z=np.where(a==0)[0]
    if len(z)>=len(b):
        r[z[:len(b)]]=b
    else:
        r[z]=b[:len(z)]
        r=np.append(r,b[len(z):])
    return r  
        

def decode_WDR(iniT,bitstream, slices,n=12,conv=2):
    k=sorted([iniT/(conv**i) for i in range(1,n+1)])
    
    bitsplit=re.split('\|',bitstream)[:-1] 
    bitsplit=bitsplit[::-1] #Le damos la vuelta ya que tiene que ir acorde con K
    
    array=0
    for i in range(n):
        subcod=re.split('(\W\d*)',bitsplit[i])
        subcod=[s for s in subcod if s!='']
        diff=[]
        value=[]
        for j in subcod:
            if j[0]=='+':
                s=1
            elif j[0]=='-':
                s=-1
            if j[1]=='0':
                value.append(s*k[i])
            elif j[1]=='1':
                value.append(s*k[i]*1.5)
                
            diff.append(int('1'+j[2:],2))
        idx=np.cumsum(diff)-1
        new_array=np.zeros(np.max(idx)+1)
        new_array[idx]=value
        if i!=0:
            array=PAD(new_array,array)
        else:
            array=new_array.copy()
    #Zero padding
    orig_len=slices[-1]['dd'].stop
    array=np.append(array,np.zeros(orig_len-len(array)))
    return array



def ALL(g,loops=12,conv=2,w='db1',nw=2,svd=135):
    A=trunc(svd,g)
    plt.imshow(A,cmap='gray')
    plt.show()
    coefs,slices,shapes=DWT(A,nw,w)
    iniT, bitstream =encode_WDR(coefs,loops,conv)
    
    arr=decode_WDR(iniT, bitstream,slices,loops,conv)
    
    Z=inverseDWT(arr,slices,shapes)
    
    fig,ax=plt.subplots(2,2,sharey='row',sharex='row')
    ax[0,0].plot(coefs)
    ax[0,1].plot(arr)
    ax[1,0].imshow(g,cmap='gray')
    ax[1,1].imshow(Z,cmap='gray')
    ax[1,0].set_axis_off()
    ax[1,1].set_axis_off()
    plt.show()
    
    return Z
    
         
            
            
    
    
    
    
    
    