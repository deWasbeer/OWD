#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 20:50:33 2023

@author: windhoos
"""

from math import pi,sqrt

def thrust():

    D = Drotor

    H = Htower
    
    rho = 1.225
    
    Ct = 0.89
    
    v = 10
    
    F = round(.5*Ct*rho*v**2*pi/4*D**2)
    Fs = "{:e}".format(F)

    M = round(F*H)
    Ms = "{:e}".format(M)

    print('Thrust:')
    
    print('F thrust '+Fs+str(' N'))
    print('M thrust '+Ms+str(' Nm'))

    return F, M

def drag():

    D = Dtower
    
    H = Htower
    
    rho = 1.225
    
    Cd = 0.5
    
    v = Vwind
    
    F = round(.5*Cd*rho*v**2*pi/4*D**2)
    Fs = "{:e}".format(F)

    M = round(F*H/2)
    Ms = "{:e}".format(M)

    print('Drag:')
    
    print('F drag '+Fs+str(' N'))
    print('M drag '+Ms+str(' Nm'))

    return F, M

def weight(D,H):

    wt = 0.07
    
    rho = 8000

    g = 9.81
    
    F = round(rho*g*pi/4*(D**2-(D-2*wt)**2)*H)
    Fs = "{:e}".format(F)

    print('Weight:')

    print('F weight '+Fs+str(' N'))

    return F
    
def morison():
    
    D = Dmp
    
    H = Hmp
    
    rho = 1000
    
    v = Vwater
    
    dv = dVwater
    
    Cm = 2
    
    Cd = .5
    
    Vol = pi/4 * D**2 * H
    
    Fm = round(rho * Cm * Vol * dv)
    Fms = "{:e}".format(Fm)

    Mm = round(Fm * H/2)
    Mms = "{:e}".format(Mm)
    
    Fd = round(0.5 * rho * Cd *  D * H * v**2)
    Fds = "{:e}".format(Fd)

    Md = round(Fd * H/2)
    Mds = "{:e}".format(Md)
    
    Fmoris = Fm + Fd
    Fmoriss = "{:e}".format(Fmoris)

    Mmoris = Mm + Md
    Mmoriss = "{:e}".format(Mmoris)

    print('Morison:')
    
    print('F Mass '+Fms+str(' N'))
    print('F Drag '+Fds+str(' N'))
    print('F Tot ' + Fmoriss+str(' N'))

    print('M Mass '+ Mms+str(' Nm'))
    print('M Drag '+ Mds+str(' Nm'))
    print('M Tot ' + Mmoriss+str(' Nm'))

    return Fmoris, Mmoris

def stress(D,wt,Fx,Fz,My):
    A=pi/4*(D**2-(D-2*wt)**2)
    I=pi/64*(D**4-(D-2*wt)**4)

    tay_xy=3*Fx/(2*A)
    tay_xys="{:e}".format(tay_xy)

    sigma_x1=Fz/A
    sigma_x1s="{:e}".format(sigma_x1)

    sigma_x2=My/I*(D/2)
    sigma_x2s="{:e}".format(sigma_x2)

    print('Stress:')

    print('tay_xy '+str(tay_xys))
    print('sigma_z '+str(sigma_x1s))
    print('sigma_x '+str(sigma_x2s))

    sigm_mises2D=round(sqrt((sigma_x1+sigma_x2)**2+3*tay_xy**2))

    print('sigma_mises '+str(round(sigm_mises2D/1e6))+' MPa')

    return sigm_mises2D

def annual():

    P = pi/4 * Drotor**2 * 1.225 * Vwind**3 * 0.89

    cf = 0.5

    time = 60*60*24*365

    E = P * time * cf
    Es = "{:e}".format(E)

    print('Annual Energy Production:')

    print('E '+Es+str(' J'))

    Ekwh = E/1000/3600
    Ekwhs = "{:e}".format(Ekwh)

    print('E '+Ekwhs+str(' kWh'))
    
def main():

    global Htower, Dtower, wttower, Drotor, Dmp, Hmp, wtmp, Vwind, Vwater, dVwater

    Drotor = 220 #m
    Htower = 150 #m
    Dtower = 8 #m
    wttower = 0.07 #m

    Dmp = 10 #m
    Hmp = 140 #m
    wtmp = 0.07 #m

    Vwind = 10 #m/s
    Vwater = 0.8 #m/s
    dVwater = 0.1 #m/s2

    print('tower')
    Fthrust,Mthrust=thrust()
    Fdrag,Mdrag=drag()
    Fweight_tower=weight(Dtower,Htower)
    sigma_tower=stress(Dtower,wttower,Fthrust+Fdrag,Fweight_tower,Mthrust+Mdrag)
    E=annual()
    print()

    print('mp')
    Fweight_tower=weight(Dtower,Htower)
    Fmoris,Mmoris=morison()
    Fweight_mp=weight(Dmp,Hmp)
    sigma_mp=stress(Dmp,wtmp,Fmoris,Fweight_mp,Mmoris)
    print()

    print('total')
    Ftot_x=Fthrust+Fdrag+Fmoris
    Ftot_z=Fweight_tower+Fweight_mp
    Mtot_y=Mthrust+Mdrag+Mmoris+(Fthrust+Fdrag)*Hmp
    sigma_tot=stress(Dmp,wtmp,Ftot_x,Ftot_z,Mtot_y)
    print()

main()
