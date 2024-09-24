#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 14:18:18 2024

@author: johan
"""

from math import exp,pi
import matplotlib.pyplot as plt
import numpy as np

def weibull(u):
    A = 11.
    k = 2.3
    pdf = k / A * ( u / A) ** ( k - 1) * exp(-(u / A) ** k )
    return pdf

def plot_weibull():
    # Generate values for the x-axis (u)
    u_values = np.linspace(0, vmax, steps)  # Adjust the range as needed

    # Calculate the corresponding PDF values
    pdf_values = [weibull(u) for u in u_values]

    # Create the plot
    plt.figure(figsize=(10, 6))  # Adjust figure size if desired
    plt.plot(u_values, pdf_values, label='Weibull Distribution')
    plt.xlabel('u')
    plt.ylabel('Probability Density Function (PDF)')
    plt.title('Weibull Distribution (A=11, k=2.3)')
    plt.legend()
    plt.grid(True)
    plt.show()

def power(v):

    vcutin = 3.
    vcutout = 30.
    
    Cp = 0.59
    
    A =  pi/4*D**2
    
    vrated = (P_rated*2/(rho_air*A*Cp))**(1/3)
    
    if v < vcutin:
        P = 0
    elif v < vrated:
        P = 0.5 * rho_air * (v)**3 * A * Cp
    elif v < vcutout:
        P = P_rated
    else:
        P = 0
        
    return P

def plot_power_curve():
    # Generate wind speed values for the x-axis
    v_values = np.linspace(0, vmax, steps)  # Adjust the range as needed

    # Calculate the corresponding power values
    power_values = [power(v) for v in v_values]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(v_values, power_values, label='Power Curve')
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('Power (W)')
    plt.title('Wind Turbine Power Curve')
    plt.legend()
    plt.grid(True)
    plt.show()
    
def calculate_annual_energy():

    # Seconds in a year
    T = 365 * 24 * 60 * 60

    # Generate wind speed values
    v_values = np.linspace(0, vmax, steps)

    # Calculate Weibull PDF and power for each wind speed
    weibull_values = [weibull(v) for v in v_values]
    power_values = [power(v) for v in v_values]

    # Calculate the integrand for each wind speed
    integrand_values = [weibull_values[i] * power_values[i] * T for i in range(steps)]

    # Numerical integration using the trapezoidal rule
    E = np.trapz(integrand_values, v_values)

    return E

def main():
    global D, rho_air,P_rated,vmax,steps
    D = 100.
    rho_air = 1.1225
    P_rated = 12*10**6
    vmax = 35
    steps = 10000
    
    plot_weibull()
    plot_power_curve()
    
    E = calculate_annual_energy()
    print(f"Annual Energy Production (E): {E:.2f} Wh")
    
main()
    