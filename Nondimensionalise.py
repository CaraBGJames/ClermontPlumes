# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 10:59:36 2021

@author: caraj
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#in SI units
Hdf = pd.read_excel('Height_data.xlsx', 'H')
Tdf = pd.read_excel('Height_data.xlsx', 'T')

#conversions
B = np.array([6.21063E-06, 5.25113E-06, 4.31039E-06, 3.54187E-06, 1.15761E-05])
M = np.array([4.58453E-05, 6.97358E-05, 6.19556E-05, 5.91024E-05, 3.88815E-05])

h = (M**(0.75))*(B**(-0.5))
t = M/B

hdf = (Hdf/100)/h
tdf = Tdf/t

leg = ["g' = 0.129, Q = 48 mL/s",
       "g' = 0.089, Q = 60 mL/s",
       "g' = 0.077, Q = 56 mL/s",
       "g' = 0.065, Q = 55 mL/s"]

plt.figure(figsize=(12,7))
plt.plot(tdf.iloc[0:-1:4,:-1], hdf.iloc[0:-1:4,:-1])
plt.title('Nondimensionalised height/time graph of circular vent plumes')
plt.xlabel('time (s) /  M$B^{-1}$ ')
plt.ylabel('height (m) /M$^{0.75}$B$^{-0.5}$')
plt.legend(leg)
plt.show()


