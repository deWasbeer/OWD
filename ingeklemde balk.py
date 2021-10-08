#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 10:37:05 2021

@author: windhoos
"""

from scipy.integrate import quad as i
import matplotlib.pyplot as p

def q(z):
    q=5.
    return q

def Ftop():
    F=50.
    return F

def F(z):
    F,acc=i(q,z,Htop)
    return F

def M(z):
    M,acc=i(F,z,Htop)
    return M

def main():
    global Htop
    Htop=100.
    
    zlist=[]
    qlist=[]
    vlist=[]
    mlist=[]
    
    steps = 100
    for step in range(steps+1):
        #z(0)=100 en z(100)=0
        z=Htop-step/steps*Htop
        zlist.append(z)
        qlist.append(q(z))
        vlist.append(F(z)+Ftop())
        mlist.append(M(z)+Ftop()*(Htop-z))
    
    p.title('Verdeelde belasting [n/m]')  
    p.grid()
    p.xlabel('q [n/m]')
    p.ylabel('z [m]')
    p.plot(qlist,zlist,'b-')
    p.show()
    p.clf()
    
    p.title('Dwarskracht [n]')
    p.grid()
    p.xlabel('V [n]')
    p.ylabel('z [m]')
    p.plot(vlist,zlist,'r-')
    p.show()
    p.clf()
    
    p.title('Moment [nm]')
    p.grid()
    p.xlabel('M [nm]')
    p.ylabel('z [m]')
    p.plot(mlist,zlist,'g-')
    p.show()
    p.clf()
main()
    