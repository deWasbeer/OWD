#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:08:54 2024

@author: johan
"""

from math import pi

def RNA():
    print('run rna')
    D_rotor = 122. #m
    W_rna = 450000. #kg
    P_rated = 12. #MW
    v_cutin = 3. #m/s
    v_cutout = 25. #m/s
    return W_rna, D_rotor

def cone(height, top_diameter, bottom_diameter):
    # Calculate the radii
    r1 = top_diameter / 2
    r2 = bottom_diameter / 2
    
    # Calculate the volume
    volume = (1/3) * pi * height * (r1**2 + r1 * r2 + r2**2)
    
    return volume

def toren(gewicht_rna, diameter_rotor):
    print('run toren')
    
    hoogte = diameter_rotor/2 + 5
    diameter_top = 3. #m
    diameter_bot = 6. #m
    wanddikte = 0.06 #m
    
    cone_buiten = cone(hoogte, diameter_top, diameter_bot)
    cone_binnen = cone(hoogte, diameter_top - 2*wanddikte, diameter_bot - 2 * wanddikte)

    V_toren = cone_buiten - cone_binnen
    M_toren = V_toren * rho_staal
    
    gewicht_onderkant_toren = gewicht_rna + M_toren
    
    return gewicht_onderkant_toren

def cilinder(D,h):
    V=pi/4*D**2*h
    return V

def monopile(W_toren):
    print('run monopile')
    H_mp = 75. #m
    wt = 0.06 #m
    
    D_mp = 7. #
    
    cilinder_buiten = cilinder(D_mp,H_mp)
    cilinder_binnen = cilinder(D_mp - 2 * wt, H_mp)
    
    V_mp = cilinder_buiten - cilinder_binnen
    W_mp = V_mp * rho_staal
    
    gewicht_onderkant_mp = W_toren + W_mp
    
    return gewicht_onderkant_mp
    
def main():
    print('run main')
    
    global rho_staal
    
    rho_staal = 8000. #kg/m3
    
    W_rna, D_rotor = RNA()
    print('gewicht RNA='+str(int(W_rna))+' kg')

    W_toren = toren(W_rna,D_rotor)
    print('gewicht RNA+toren='+str(int(W_toren))+' kg')
    
    W_mp = monopile(W_toren)
    print('gewicht RNA+toren+mp='+str(int(W_mp))+' kg')

main()