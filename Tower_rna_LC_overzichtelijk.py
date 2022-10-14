#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 12:49:20 2022

@author: windhoos
"""

def Dtower(z,Dmax,Dmin,hint,hrna):
    a=(Dmin-Dmax)/(hrna-hint)
    b=Dmin-a*hrna
    D=a*z+b
    return D

def main():
    Dmax=12.
    Dmin=6.0
    hrna=100.
    hint=10.
    
    D=Dtower(hrna,Dmax,Dmin,hint,hrna)
    print(D)
    
main()
    
