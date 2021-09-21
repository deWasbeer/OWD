#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 12:28:38 2021

@author: windhoos
"""

from math import pi,log10
from scipy.integrate import quad as q
from tabulate import tabulate as t

def RNA(D,v,vrated,rho,LC):
    if LC == 0:
        Ct=0.89
        A=pi/4.*D**2
        F=.5*rho*Ct*A*vrated**2
    else:
        Ablade=0.5*3*D/2.
        Cd=1.0
        F=0.5*Cd*3*Ablade*v**2*rho
        
    return F

def Dtower(z,Dtop,Dint,Htop,Hint):
    a=(Dint-Dtop)/(Hint-Htop)
    b=Dtop-a*Htop
    Dtower=a*z+b
    return Dtower

def wind(z,z0,Vref,Href):
    V=Vref*(log10(z/z0))/(log10(Href/z0))
    return V

def Drag_dz(z,v,rho,Dtop,Dint,Htop,Hint,z0,Vref,Href,Cd):
    F=Cd*.5*rho*Dtower(z,Dtop,Dint,Htop+Hint,Hint)*v**2
    return F

def main():
    Dint,Hint=6.,20,
    Drna,Hrna=3.,120.
    Vref,Href=10.,10.
    z0=0.0002
    vrated=12.
    Cd=1.0
    Drotor=120.
    rho=1.025
    Loads=[[['hoogte [m]','windsneldheid [m/s]','belasting [kN]']],[['hoogte [m]','windsneldheid [m/s]','belasting [kN]']],[['hoogte [m]','windsneldheid [m/s]','belasting [kN]']]]
    for LC in range(3):
        for i in range(101):
            z=Hrna-i/100*Hrna+Hint
            v=wind(z,z0,Vref,Href)
            if LC == 0:
                v=v
            elif LC == 1:
                v=v*5*1.2
            elif LC == 2:
                v=v*5
            Frna=RNA(Drotor,wind(Hint+Hrna,z0,Vref,Href),vrated,rho,LC)
            Ftower=q(Drag_dz,z,Hrna+Hint,args=(v,rho,Drna,Dint,Hrna,Hint,z0,Vref,Href,Cd))
            if LC == 0:
                Loads[0].append([round(z,0),round(v,0),round((Frna+Ftower[0]/1000.),0)])
            elif LC == 1:
                Loads[1].append([round(z,0),round(v,0),round((Frna+Ftower[0]/1000.),0)])
            elif LC == 2:
                Loads[2].append([round(z,0),round(v,0),round((Frna+Ftower[0]/1000.),0)])
    print('LOADCASE 1')
    print(t(Loads[0]))
    print('LOADCASE 2')
    print(t(Loads[1]))
    print('LOADCASE 3')
    print(t(Loads[2]))
main()
