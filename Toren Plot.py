# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 13:06:38 2020

@author: antoj
@youtube: https://www.youtube.com/watch?v=5yb48Ltu5Jo
"""

from math import log10
import matplotlib.pyplot as plt
from scipy.integrate import quad

def Dtower(z,Dtop,Dint,Htop,Hint):
    a=(Dint-Dtop)/(Hint-Htop)
    b=Dtop-a*Htop
    Dtower=a*z+b
    return Dtower

def wind(z,z0,Vref,Href):
    V=Vref*(log10(z/z0))/(log10(Href/z0))
    return V

def Drag_dz(z,rho,Dtop,Dint,Htop,Hint,z0,Vref,Href,Cd):
    F=Cd*.5*rho*Dtower(z,Dtop,Dint,Htop,Hint)*wind(z,z0,Vref,Href)**2
    return F

def Mdrag_dz(z,rho,Dtop,Dint,Htop,Hint,z0,Vref,Href,Cd):
    F,acc=quad(Drag_dz,z,Htop,args=(rho,Dtop,Dint,Htop,Hint,z0,Vref,Href,Cd))
    return F

def main():
    rho=1.225 #kg/m3
    z0=0.0002 #m
    Vref=10. #m/s
    Href=100. #m/s
    Dtop=5. #m
    Dbot=8. #m
    Htop=Href #m
    Hint=10. #m
    Cd=1.0 #-
    
    zlist=[]
    Dlist=[]
    vlist=[]
    Flist=[]
    Mlist=[]
    
    for z in range(101):
        hoogte=Hint+(Htop-Hint)*z/100.
        zlist.append(hoogte)
        Dlist.append(Dtower(hoogte,Dtop,Dbot,Htop,Hint))
        vlist.append(wind(hoogte,z0,Vref,Href))
        F,acc=quad(Drag_dz,hoogte,Htop,args=(rho,Dtop,Dbot,Htop,Hint,z0,Vref,Href,Cd))
        Flist.append(F)
        M,acc=quad(Mdrag_dz,hoogte,Htop,args=(rho,Dtop,Dbot,Htop,Hint,z0,Vref,Href,Cd))
        Mlist.append(M)
    
    print(Dlist)
    print(zlist)
    print(vlist)
    print(Flist)
    print(Mlist)
    
    plt.plot(Dlist, zlist, 'b-')
    plt.title('Toren')
    plt.xlabel('Diameter [m]')
    plt.ylabel('Hoogte (z) [m]')
    plt.savefig('Toren.png', dpi=300)
    plt.clf()
    
    plt.plot(vlist, zlist, 'g-')
    plt.title('Wind verloop')
    plt.xlabel('Wind snelheid [m/s]')
    plt.ylabel('Hoogte (z) [m]')
    plt.savefig('Wind.png', dpi=300)
    plt.clf()
    
    plt.plot(Flist, zlist, 'r-')
    plt.title('Kracht op toren')
    plt.xlabel('Kracht [N]')
    plt.ylabel('Hoogte (z) [m]')
    plt.savefig('Kracht.png', dpi=300)
    plt.clf()
    
    plt.plot(Mlist, zlist, 'g-')
    plt.title('Moment op toren')
    plt.xlabel('Moment [Nm]')
    plt.ylabel('Hoogte (z) [m]')
    plt.savefig('Moment.png', dpi=300)
    plt.clf()
    
main()