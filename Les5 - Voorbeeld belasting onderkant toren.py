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

from math import log

def Force(Htop,Hbot,c1,c2,c3,c4,c5,c6,c7,c8):
    x=Htop
    Ftop=1./(4*c4**2*log(10)**2)*c1*c2**2*x*(2*(log(x/c3))**2*(c5*x+2*c6-2*c7*c8)-2*log(x/c3)*(c5*x+4*c6-4*c7*c8)+c5*x+8*c6-8*c7*c8)
    x=Hbot
    Fbot=1./(4*c4**2*log(10)**2)*c1*c2**2*x*(2*(log(x/c3))**2*(c5*x+2*c6-2*c7*c8)-2*log(x/c3)*(c5*x+4*c6-4*c7*c8)+c5*x+8*c6-8*c7*c8)
    F=Ftop-Fbot
    return F

def main():
    #In dit voorbeeld wordt de berekende kracht als gevolg van ALLEEN de wind belasting op de toren van de windturbine bepaald.
    #Vul hier zelf jou onderstaande waarden in, let op refereer al je hoogtes tov de MSL.
    #Dit programma hoort bij slide 20 van les 5 en dient als voorbeeld om overige krachtenen momenten te berekenen.
    Cd=
    rho=
    Href=
    z0=
    Dmin=
    Dmax=
    Hrna=
    Hint=
    c1=.5*Cd*rho
    c2=Href
    c3=z0
    c4=log(Href/z0)
    c5=(Dmin-Dmax)/(Hrna-Hint)
    c6=Dmax
    c7=c5
    c8=Hint
    F=Force(Htop,Hbot,c1,c2,c3,c4,c5,c6,c7,c8)
    print(F)
main()