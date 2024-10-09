#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:04:40 2024

@author: johan
"""

from math import pi
from scipy.integrate import quad
import matplotlib.pyplot as plt

def plot(z_values, F_values, name, horizontal_text):
    """
    Creates a graph of F (integral of drag force) vs. z (height).

    Args:
      z_values: A list of height values (z).
      F_values: A list of corresponding integral of drag force values (F).
    """

    plt.plot(F_values, z_values, linestyle='-')  # Swapped F_values and z_values
    plt.xlabel(horizontal_text)  # Updated x-axis label
    plt.ylabel("Height (m)")  # Updated y-axis label
    plt.title(name)
    plt.grid(True)
    plt.show()

def D_inertia(z):
    #let op tov mudline als z=0
    if z < Hbay2_top:
        D = 8
    elif z <= Water_depth:
        D = 10.
            
    return D

def D_drag(z):
    #let op tov mudline als z=0
    #let op tov mudline als z=0
    if z < Hbay2_top:
        D = 8
    elif z <= Water_depth:
        D = 10.
        
    return D

def water_speed(z):
    #let op tov mudline als z=0
    V = z**2 * 1/625
    return V

def water_acceleration(z):
    #let op tov mudline als z=0
    dV = 0.5 * z**2 * 1/625
    return dV

def dF_morison(z):
    
    C1 = rho_water * Cm * pi / 4
    C2 = rho_water * Cd / 2
    
    dF_inertia = C1 * D_inertia(z)**2 * water_acceleration(z)
    
    dF_drag = C2 * D_drag(z) * abs(water_speed(z)) * water_speed(z)
    
    dF_tot = dF_inertia + dF_drag
    
    return dF_tot

def F_morison(z):
    F,acc = quad(dF_morison, z, Water_depth)
    return F

def M_morison(z):
    M,acc = quad(F_morison, z, Water_depth)
    return M

def main():
    
    global rho_water, Cm, Cd
    global Hbay2_bot,Hbay2_top,Hbay1_bot,Hbay1_top, Water_depth
    rho_water = 1.225 #kg/m3
    Cm = 2.
    Cd = 1.
    
    Hbay2_bot = 0
    Hbay2_top = 15
    Hbay1_bot = Hbay2_top
    Hbay1_top = 30
    Water_depth = Hbay1_top - 5
    
    #z = (from Htop to Hbot)
    z_values = [z for z in range(int(Water_depth), int(Hbay2_bot) - 1, -1)]
    
    #F = integral(drag(z,LC),Htop -> z)
    F_values = []
    M_values = []
    for z in z_values:
        # Calculate the definite integral of drag(z, LC) from Htop to z
        F_values.append(F_morison(z))
        M_values.append(M_morison(z))
        
    plot(z_values,F_values,"Water force jacket", "Force (N)")
    plot(z_values,M_values,"Water moment jacket","Moment (Nm)")
    
main()
























