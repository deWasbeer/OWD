# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 12:32:50 2018

@author: Johan Antonissen j.antonissen@hr.nl

In het volgende rekenmodel worden de benodigde berekeningen gemaakt voor de module offshore windfarm design,
de 4e jaars module van de opleiding werktuigbouwkunde van de Hogeschool Rotterdam.
 
Naast dit overkoepelende bestand zullen er 10 deelbestanden zijn waar de berekeniningen behorende bij de les worden uitgevoerd.

Les 5 - Loads:

- Loadcases
- RNA loads
- Tower loads
- Tower stresses
- Tower design
- Monopile loads
- Monopile stresses
- Monopile design
"""
from scipy.optimize import brentq
from math import pi, sqrt

def area(wt,D):
    A=pi/4.*(D**2-(D-2*wt)**2)
    return A
        
def inertia(wt,D):
    r=D/2.
    I=pi/4.*((r**4-(r-wt)**4))
    return I
        
def sigma(wt,D,fx,fz,my):
    r=D/2.
    sigm=sqrt((fz/area(wt,D)+my*r/inertia(wt,D))**2+3*((fx/area(wt,D))**2))
    return sigm
        
def wt_minimizer(wt,D,fx,fz,my,sigm_steel):
    sigm=sigma(wt,D,fx,fz,my)
    return sigm-sigm_steel*10**6


def main():
    continue_loop = 'yes'
    while continue_loop == 'yes':
        D=float(input('Diameter segment [m] ? '))
        fx=float(input('Fx: Kracht parallel aan wind [N] ? '))
        fz=float(input('Fz: Kracht omlaag door gewicht [N] ? '))
        my=float(input('My: Moment om y-as door Fx [Nm] ? '))
        sigm_yield=float(input('Vloeispanning van materiaal [N/mm²] ? '))
        wt=brentq(wt_minimizer,0.0000000001,D/2-.01,args=(D,fx,fz,my,sigm_yield))
        print(int(D*10)/10., 'm')
        print(int(fx*10)/10., 'N')
        print(int(fz*10)/10., 'N')
        print(int(my*10)/10., 'Nm')
        print(int(wt*10.*1000)/10., 'mm wanddikte voor gegeven spanning')
        print()        
        print('Wil je doorgaan met de berekening? ')
        vraag=input('Druk enter voor ja ')
        if vraag != '':
            continue_loop = 'no'
            print()
main()
