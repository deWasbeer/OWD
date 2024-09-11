#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 14:56:49 2024

@author: johan
"""

import matplotlib.pyplot as plt
from math import log10

# Define the function
def wind_profile(z):
    if z > 0:
        V = Vref * log10(z / z0) / log10(Href / z0)
    else:
        V = 0
    return V

global z0, Href, Vref

def loadcase(lc, z):
    if lc == 2:
        V = wind_profile(z) * 5 * 1.09
    elif lc == 3:
        V = wind_profile(z) * 5 * 1.2
    return V

z0 = 0.0002
Href = 100
Vref = 10

# Lists to store x and y values
x_values = []
LC2_values = []
LC3_values = []

# Populate the lists using a for loop
for i in range(1001):  # From 0 to 100 inclusive, step 0.1
    h = i / 10
    x_values.append(h)
    LC2_values.append(loadcase(2, h))
    LC3_values.append(loadcase(3, h))

# Plotting
plt.plot(LC2_values, x_values, label='LC2', color='blue')
plt.plot(LC3_values, x_values, label='LC3', color='red')

# Adding title and labels
plt.title('Wind Profile for Load Cases LC2 and LC3')
plt.xlabel('Wind Speed [m/s]')
plt.ylabel('Height [m]')

# Adding grid and legend
plt.grid(True)
plt.legend()

# Show plot
plt.show()
