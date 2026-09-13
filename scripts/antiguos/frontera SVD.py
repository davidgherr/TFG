# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 21:14:12 2022

@author: david
"""

import numpy as np
import matplotlib.pyplot as plt

m=np.array([i for i in range(264)])
n=np.array([i for i in range(264)])


plt.plot((m*n)/(m+n+1))

plt.show()

def f(m,n):
    return m*n/(m+n+1)
