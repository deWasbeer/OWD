# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 15:04:50 2021

@author: windh
"""

from math import log10
from scipy.integrate import quad
import matplotlib.pyplot as plt

def wind(z):
    u=vref*log10(z/z0)/log10(href/z0)
    return u

def diameter(z):
    #a=-2./105
    #b=6+2./105*120
    a=-1/20.
    b=3-a*120.
    D=a*z+b
    if D >= 4:
        D=4
    return D

def D_drag(z):
    #F=0.5*rho*D*H*v**2*Cd [N]
    dF=0.5*rho*diameter(z)*wind(z)**2*Cd #N/m
    return dF

def Fdrag(z):
    F,acc = quad(D_drag, z, Hrna)
    return F

def Mdrag(z):
    M,acc = quad(Fdrag, z, Hrna)
    return M

def main():
    #onze constanten
    global z0,href,vref,rho,Cd
    z0=0.0002
    href=10.
    vref=5.
    rho=1.225
    Cd=1.
    
    global Hint,Hrna
    Htower = 105. #hoogte toren
    Hint = 15. #tov MSL
    Hrna= Htower + Hint #tov MSL
    
    zlist=[]
    Dlist=[]
    Flist=[]
    Mlist=[]
    
    steps = 100
    for step in range(steps+1):
        #we zoeken een bereik van 120 tot 15 in 100 stappen
        z=Hrna-step/steps*Htower
        zlist.append(round(z,1))
        Dlist.append(round(diameter(z),3))
        F=Fdrag(z)
        Flist.append(round(F,1))
        M=Mdrag(z)
        Mlist.append(round(M,1))
    
    plt.title('Toren Diameter')
    plt.xlabel('Diameter [m]')
    plt.ylabel('Hoogte [m]')
    plt.plot(Dlist,zlist)
main()