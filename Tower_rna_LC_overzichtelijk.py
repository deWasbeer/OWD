#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 11:47:21 2022

@author: windhoos
"""

from math import log10
from scipy.integrate import quad as q
import matplotlib.pyplot as plt

def windspeed(z,vref,href,z0):
    v=vref*log10(z/z0)/log10(href/z0)
    return v

def F_rna_lc_1(rho,v_rated,A_disk,Ct):
    F=0.5*rho*v_rated**2*A_disk*Ct
    return F

def F_rna_lc_2(rho,Ablade,Cd,hrna,vref,href,z0):
    v=windspeed(hrna,vref,href,z0)*5*1.09
    F=0.5*rho*v**2*3*Ablade*Cd
    return F

def F_rna_lc_3(rho,Ablade,Cd,hrna,vref,href,z0):
    v=windspeed(hrna,vref,href,z0)*5*1.2
    F=0.5*rho*v**2*3*Ablade*Cd
    return F

def stap1_rna(rho_air,v_rated,A_disk,A_blade,Ct,Cd,hrna,vref,href,z0):
    F1=F_rna_lc_1(rho_air,v_rated,A_disk,Ct)
    F2=F_rna_lc_2(rho_air,A_blade,Cd,hrna,vref,href,z0)
    F3=F_rna_lc_3(rho_air,A_blade,Cd,hrna,vref,href,z0)
    return F1,F2,F3

def Dtower(z,Dmax,Dmin,hint,hrna):
    a=(Dmin-Dmax)/(hrna-hint)
    b=Dmin-a*hrna
    D=a*z+b
    return D

def fdrag(z,rho,Cd,vref,href,z0,Dmax,Dmin,hint,hrna,LC):
    
    if LC==0:
        const=1.
    elif LC==1:
        const=5*1.09
    elif LC==2:
        const=5*1.2
        
    dF=1.5*Cd*rho*const*windspeed(z,vref,href,z0)**2*Dtower(z,Dmax,Dmin,hint,hrna)
    return dF

def mdrag(z,rho,Cd,vref,href,z0,Dmax,Dmin,hint,hrna,LC):
    F,acc=q(fdrag,z,hrna,args=(rho,Cd,vref,href,z0,Dmax,Dmin,hint,hrna,LC))
    return F

def stap2_toren(hrna,hint,rho,Cd,vref,href,z0,Dmax,Dmin,stappen):
    zlist=[[],[],[]]
    flist=[[],[],[]]
    mlist=[[],[],[]]
    
    for LC in range(3):
        for i in range(stappen+1):
            z=hint+(hrna-hint)*i/stappen
            F,acc=q(fdrag,z,hrna,args=(rho,Cd,vref,href,z0,Dmax,Dmin,hint,hrna,LC))
            M,acc=q(mdrag,z,hrna,args=(rho,Cd,vref,href,z0,Dmax,Dmin,hint,hrna,LC))
            
            zlist[LC].append(z)
            flist[LC].append(F)
            mlist[LC].append(M)
            
    return zlist,flist,mlist

def D_tp_mp(z):
    if z <= 0:
        D=12
    elif z > 0:
        D=8
    return D
    
'''
def stap3_tp():
    F_LC1()
    F_LC2()
    F_LC3()
    return F

def stap4_mp():
    F_LC1()
    F_LC2()
    F_LC3()
    return F
'''

def main():
    rho_air=1.225 #kg/m3
    v_rated=15. #m/s
    A_disk=43742. #m2
    D_rotor=236. #m
    A_blade=3*D_rotor/2.*0.5
    Ct=0.89 #-
    Cd=1. #-
    
    hrna=125. #m
    hint=10. #m
    vref=9.47 #m/s
    href=10. #m/s
    z0=0.0002 #m/s
    
    Dmin=5. #m
    Dmax=12. #m
    
    stappen=100
    
    F1,F2,F3=stap1_rna(rho_air,v_rated,A_disk,A_blade,Ct,Cd,hrna,vref,href,z0)
    
    zlist_rna=[[],[],[]]
    flist_rna=[[],[],[]]
    mlist_rna=[[],[],[]]
    for LC in range(3):
        for i in range(stappen+1):
            z=hint+(hrna-hint)*i/stappen
            zlist_rna[LC].append(z)
            if LC == 0:
                F=F1
                M=F1*(hrna-z)
            elif LC == 1:
                F=F2
                M=F2*(hrna-z)
            elif LC == 2:
                F=F3
                M=F3*(hrna-z)
            
            flist_rna[LC].append(F)
            mlist_rna[LC].append(M)
            
    plt.plot(flist_rna[0], zlist_rna[0], 'r-')
    plt.plot(flist_rna[1], zlist_rna[1], 'g-')
    plt.plot(flist_rna[2], zlist_rna[2], 'b-')
    plt.title('Kracht op rna')
    plt.xlabel('Kracht [N]')
    plt.ylabel('Hoogte (z) [m]')
    plt.show()
    #plt.savefig('Kracht.png', dpi=300)
    plt.clf()
    
    plt.plot(mlist_rna[0], zlist_rna[0], 'r-')
    plt.plot(mlist_rna[1], zlist_rna[1], 'g-')
    plt.plot(mlist_rna[2], zlist_rna[2], 'b-')
    plt.title('Moment op rna')
    plt.xlabel('Moment [Nm]')
    plt.ylabel('Hoogte (z) [m]')
    plt.show()
    #plt.savefig('Moment.png', dpi=300)
    plt.clf()  
    
    zlist_tower,flist_tower,mlist_tower=stap2_toren(hrna,hint,rho_air,Cd,vref,href,z0,Dmax,Dmin,stappen)
    
    plt.plot(flist_tower[0], zlist_tower[0], 'r-')
    plt.plot(flist_tower[1], zlist_tower[1], 'g-')
    plt.plot(flist_tower[2], zlist_tower[2], 'b-')
    plt.title('Kracht op toren')
    plt.xlabel('Kracht [N]')
    plt.ylabel('Hoogte (z) [m]')
    plt.show()
    #plt.savefig('Kracht.png', dpi=300)
    plt.clf()
    
    plt.plot(mlist_tower[0], zlist_tower[0], 'r-')
    plt.plot(mlist_tower[1], zlist_tower[1], 'g-')
    plt.plot(mlist_tower[2], zlist_tower[2], 'b-')
    plt.title('Moment op toren')
    plt.xlabel('Moment [Nm]')
    plt.ylabel('Hoogte (z) [m]')
    plt.show()
    #plt.savefig('Moment.png', dpi=300)
    plt.clf()
    
    zlist_rna_tower=[[],[],[]]
    flist_rna_tower=[[],[],[]]
    mlist_rna_tower=[[],[],[]]
    for LC in range(3):
        for i in range(stappen+1):
            z=hint+(hrna-hint)*i/stappen
            zlist_rna_tower[LC].append(z)

            F=flist_rna[LC][i]+flist_tower[LC][i]
            M=mlist_rna[LC][i]+mlist_tower[LC][i]
                
            flist_rna_tower[LC].append(F)
            mlist_rna_tower[LC].append(M)
            
    plt.plot(flist_rna_tower[0], zlist_rna_tower[0], 'r-')
    plt.plot(flist_rna_tower[1], zlist_rna_tower[1], 'g-')
    plt.plot(flist_rna_tower[2], zlist_rna_tower[2], 'b-')
    plt.title('Kracht op rna+toren')
    plt.xlabel('Kracht [N]')
    plt.ylabel('Hoogte (z) [m]')
    plt.show()
    #plt.savefig('Kracht.png', dpi=300)
    plt.clf()
    
    plt.plot(mlist_rna_tower[0], zlist_rna_tower[0], 'r-')
    plt.plot(mlist_rna_tower[1], zlist_rna_tower[1], 'g-')
    plt.plot(mlist_rna_tower[2], zlist_rna_tower[2], 'b-')
    plt.title('Moment op rna+toren')
    plt.xlabel('Moment [Nm]')
    plt.ylabel('Hoogte (z) [m]')
    plt.show()
    #plt.savefig('Moment.png', dpi=300)
    plt.clf()  
    
    #stap3_tp()
    #stap4_mp()
main()
