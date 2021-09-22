# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 16:26:20 2020

@author: antoj
"""

from math import pi,exp,log10
import scipy.integrate as integrate
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

def powercurve(v,D,Prated,rho,Cd,vcutin,vcutout):
    A=pi/4.*D**2
    P=1/2.*Cd*rho*(v-vcutin)**3*A/(10**6)
    
    if P < 0:
        return 0.
    elif v >= vcutout:
        return 0.
    elif P < Prated:
        return P
    elif P >= Prated:
        return Prated
    
def weibull(v,A,k):
    pdf=k/A*(v/A)**(k-1)*exp(-(v/A)**k)
    return pdf

def energy(v,D,Prated,rho,Cd,vcutin,vcutout,A,k):
    E=powercurve(v,D,Prated,rho,Cd,vcutin,vcutout)*weibull(v,A,k)*60*60*24*365/(10**9)
    return E

def windscale(z,Vref,Href,z0):
    Vz=Vref*(log10(z/z0))/(log10(Href/z0))
    return Vz
    
def main():   
    D=120. #m
    Prated=12. #mw
    
    rho=1. #kg/m3
    A= 15 #m/s
    k=3 #-
    z0=0.0002 #m
    Cd=0.59 #-
    vcutin=3. #m/s
    vcutout=35 #m/s
    steps=50 #-
    
    vlist=[]
    plist=[]
    pdflist=[]
    elist=[]
    for v in range(steps):
        Anacelle=windscale(100,A,10,z0)
        vlist.append(v)
        plist.append(powercurve(v,D,Prated,rho,Cd,vcutin,vcutout))
        pdflist.append(weibull(v,Anacelle,k))
        E=integrate.quad(energy, 0, v, args=(D,Prated,rho,Cd,vcutin,vcutout,Anacelle,k))
        elist.append(E[0])
    #print(elist)
        
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)
    
    par1 = host.twinx()
    par2 = host.twinx()
    
    offset = 30
    
    new_fixed_axis = par1.get_grid_helper().new_fixed_axis
    par1.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par1,
                                        offset=(0, 0))
    
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(offset, 0))
    
    par2.axis["right"].toggle(all=True)
    
    host.set_xlim(0, steps)
    host.set_ylim(0, 1.1*max(plist))
    
    host.set_xlabel("speed (m/s)")
    host.set_ylabel("power (GW)")
    par1.set_ylabel("pdf (-)")
    par2.set_ylabel("energy sum (PJ)")
    
    p1, = host.plot(vlist,plist,label="power (GW)")
    p2, = par1.plot(vlist,pdflist,label="pdf (-)")
    p3, = par2.plot(vlist,elist,label="energy (GJ)")
    
    par1.set_ylim(0, 1.1*max(pdflist))
    par2.set_ylim(0, 1.1*max(elist))
    
    host.legend()
    
    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())
    
    plt.draw()
    plt.savefig('Weibull-Power-Eenergy.png', bbox_inches='tight')
    plt.show()
    plt.clf()
    
main()
