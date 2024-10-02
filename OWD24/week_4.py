#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 10:17:31 2024

@author: johan
"""
from math import log10, pi
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

def wind(z, LC):
    #tov MSL
    if LC == 1:
        V = Vrna * log10(z/z0) / log10(Hrna/z0)
    else:
        # zelf aanpassen
        V = Vref * log10(z/z0) / log10(Href/z0)
    return V

def thrust(z,LC):
    A_disk = pi/4 * D_rotor**2
    F = 0.5 * rho_air * A_disk * wind(z,LC)**2 * Ct
    return F

def turbine(z,LC):
    if LC == 1:
        F = thrust(z,LC)
    else:
        # zelf aanpassen
        F = None
    return F

def D_toren(z):
    Dtop = Dtower_top
    Htop = Htower_top
    Dbot = Dtower_bot
    Hbot = Htower_bot
    
    a = (Dtop - Dbot) / (Htop - Hbot)
    b = Dtop - a * Htop
    
    D = a * z + b
    
    return D

def drag(z, LC):
    #         kg / m3 * m * (m/s)**2 = kg / s**2 = N / m
    dF = 0.5 * rho_air * Cd_toren * D_toren(z) * wind(z,LC)**2
    return dF

def toren(LC):
    Htop = Htower_top
    Hbot = Htower_bot
    
    #z = (from Htop to Hbot)
    z_values = [z for z in range(int(Htop), int(Hbot) - 1, -1)] 
    
    #F = integral(drag(z,LC),Htop -> z)
    F_values = []
    M_values = []
    for z in z_values:
        # Calculate the definite integral of drag(z, LC) from Htop to z
        integral_result, _ = quad(drag, z, Htop, args=(LC,))  
        F_values.append(integral_result)
        
        # Calculate the moment by integrating z * drag(z, LC) from Htop to z
        def moment_integrand(z, LC):
            return (Hrna - z) * drag(z, LC)
        moment_result, _ = quad(moment_integrand, z, Htop, args=(LC,))
        M_values.append(moment_result)
        
    plot(z_values,F_values,"Wind force tower", "Force (N)")
    plot(z_values,M_values,"Wind moment tower","Moment (Nm)")
    
    return F_values[-1], M_values[-1]

def substructure():
    pass

def S(number):
  return "{:.2e}".format(number)

def main():
    global z0, Href, Vref, rho_air, rho_water, D_rotor
    global Ct, Cd_toren, Cd_substructure, Cm, Hrna, Vrna
    global Dtower_top, Htower_top, Dtower_bot, Htower_bot
    
    z0 = 0.0002
    Href = 100.
    Vref = 10.
    Hrna = 150.
    Vrna = 15.
    D_rotor = 120.
    Ct = 0.89
    rho_air = 1.225
    Cd_toren = 0.5
    
    Dtower_top = 5.
    Dtower_bot = 10.
    Htower_top = Hrna # boven MSL
    Htower_bot = 20. # boven MSL
    
    F_turbne_LC1 = turbine(Hrna,1)
    print('------- RNA -------')
    print('F thrust LC1 = ',S(F_turbne_LC1), ' N')
    print('------- RNA -------')
    print()
    print('------- tower -------')
    F_toren_LC1, M_toren_LC1 = toren(1)
    print('F tower LC1 = ',S(F_toren_LC1), ' N')
    print('M tower LC1 = ',S(M_toren_LC1), ' Nm')
    F_total = F_turbne_LC1 + F_toren_LC1
    M_total = M_toren_LC1 + F_turbne_LC1 * (Htower_top - Htower_bot)
    print('F total LC 1 =',S(F_total), ' N')
    print('M total LC 1 =',S(M_total), ' Nm')
    print('------- tower -------')
    substructure()

main()