# -*- coding: utf-8 -*-
"""
Created on Tue May  8 14:02:53 2018

@author: johan antonissen
"""

import matplotlib.pyplot as plt
from math import log,sqrt,pi,tanh,cosh,sinh,cos,sin
import numpy as np
from scipy import optimize

class wave:
    def __init__(self,Hwater,Hss50m,Hw50m,Tw50m,Hsta,Uc1m):
        self.Hdepth=Hwater #Waterdiepte m
        self.Hss50m=Hss50m #Storm sturge 50 year max m
        self.Hw50m=Hw50m #Wave height 50 year max
        self.Tw50m=Tw50m #Wave period 50 year max
        self.Hstm=Hsta*1.86 #Spring tide average (needs *1,86 for max)
        
        self.Hmax_50_year = 0.0
        self.H50 = 0.0
        self.Tmax_50_year = 0.0
        self.kmax_50_year = 0.0
        self.Hmax_50_year = 0.0
        self.Tpeak_50_year = 0.0
        self.Uw_50_year = 0.0
                                              
        self.Hred_50_year = 0.0
        self.Tred_50_year = 0.0
        self.kred_50_year = 0.0
        self.Hred_50_year = 0.0
        
        self.Hmax_1_year = 0.0
        self.Tmax_1_year = 0.0
        self.kmax_1_year = 0.0
        self.Hmax_1_year = 0.0
        
        self.Hmax_water_depth = 0.0
        
        self.Uc1m = Uc1m #1 year max current m/s
        
        self.g=9.81
        
        self.H=[]
        
    def max_natte_zone(self,mean_sea_level,storm_surge_max50,wave_height_max50,spring_tide_max50):
        return mean_sea_level+storm_surge_max50+0.65*wave_height_max50+spring_tide_max50/2.
        
    def current_profile(self,z,U0):
        d=self.Hdepth
        return U0*(z/d)**.8
        
    def golf_snelheid(self,t,z,loadcase):
        wave_period=1./(self.wave_frequency(loadcase))
        return self.wave_amplitude(loadcase)*self.wave_frequency(loadcase)*cosh(self.wave_number(wave_period)*(z+self.Hdepth))/sinh(self.wave_number(wave_period)*self.Hdepth)*cos(-self.wave_frequency(loadcase)*t)
        
    def golf_acceleratie(self,t,z,loadcase):
        wave_period=1./(self.wave_frequency(loadcase))
        return self.wave_amplitude(loadcase)*self.wave_frequency(loadcase)**2*cosh(self.wave_number(wave_period)*(z+self.Hdepth))/sinh(self.wave_number(wave_period)*self.Hdepth)*sin(-self.wave_frequency(loadcase)*t)
        
    def hydrodynamic_conditions(self):
        Hmax_50_year = self.Hss50m
        self.H50=Hmax_50_year/2.5
        self.Tmax_50_year = 11.1 * sqrt(Hmax_50_year / 9.81)
        self.kmax_50_year = self.wave_number(self.Tmax_50_year)
        self.Hmax_50_year = min(Hmax_50_year, self.wave_limit(self.kmax_50_year))
        self.Tpeak_50_year = 1.4 * 11.1 * sqrt(self.H50 / 9.81)
        #self.Uw_50_year = (pi * self.H50 / (self.Tpeak_50_year * sinh(self.wave_number(self.Tpeak_50_year) * self.Hdepth)))
                                              
        Hred_50_year = 1.32 * self.H50
        self.Tred_50_year = 11.1 * sqrt(Hred_50_year / 9.81)
        self.kred_50_year = self.wave_number(self.Tred_50_year)
        self.Hred_50_year = min(Hred_50_year, self.wave_limit(self.kred_50_year))
        
        Hmax_1_year = 1.86 * self.H50
        self.Tmax_1_year = 11.1 * sqrt(Hmax_1_year / 9.81)
        self.kmax_1_year = self.wave_number(self.Tmax_1_year)
        self.Hmax_1_year = min(Hmax_1_year, self.wave_limit(self.kmax_1_year))
        
    def wave_number(self, period):
        omega = 2 * pi / period
        
        start_k = omega**2 / self.g
        return optimize.newton(self.dispersion, start_k, args = (omega, ), tol = 0.001)
    
    def dispersion(self, d, *args):
        k = d
        omega = args[0]
        return omega**2 - self.g * k * tanh(k * self.Hdepth)
    
    def wave_limit(self, k):
        shallow_water_limit = 0.78 * self.Hdepth
        deep_water_limit = 0.142 * 2.0 * pi /k
        return min(shallow_water_limit, deep_water_limit)
        
    def wave_length(self,depth):
        if depth >=20.:
            #deep
            lampda=2*depth
        elif depth >= 10. :
            #intermediate
            lampda=10*depth
        else: 
            #shallow
            lampda=20*depth
        return lampda
        
    def wave_amplitude(self,loadcase):
        if loadcase == '50max':
            amplitude=self.Hmax_50_year
        elif loadcase == '50red':
            amplitude = self.Hred_50_year
        elif loadcase == '1max':
            amplitude = self.Hmax_1_year
        return amplitude
        
    def wave_frequency(self,loadcase):
        if loadcase == '50max':
            freq=1./self.Tmax_50_year
        elif loadcase == '50red':
            freq = 1./self.Tred_50_year
        elif loadcase == '1max':
            freq = 1./self.Tmax_1_year
        return freq
        
    def current_speed(self,Ucurrent1max,loadcase):
        if loadcase == '50max':
            U=Ucurrent1max*1.2
        elif loadcase == '50red':
            U=Ucurrent1max*1.09
        elif loadcase == '1max':
            U=Ucurrent1max
        return U
        
    def current_profile_plot(self,Hmax,max_water_data):
        H=[[],[],[],[],[],[],[]]
        for hoogte in range(int(Hmax)+1):
            U1max=self.current_profile(hoogte,max_water_data[0][0])
            Udot1max=self.current_profile(hoogte,max_water_data[0][1])
            U50red=self.current_profile(hoogte,max_water_data[1][0])
            Udot50red=self.current_profile(hoogte,max_water_data[1][1])
            U50max=self.current_profile(hoogte,max_water_data[2][0])
            Udot50max=self.current_profile(hoogte,max_water_data[2][1])
            H[0].append(-Hmax+hoogte)
            H[1].append(U1max)
            H[2].append(Udot1max)
            H[3].append(U50red)
            H[4].append(Udot50red)
            H[5].append(U50max)
            H[6].append(Udot50max)
        plt.clf()
        plt.plot(H[1],H[0],'r-',label='U1m')
        plt.plot(H[2],H[0],'r--',label='dU1m')
        plt.plot(H[3],H[0],'b-',label='U50r')
        plt.plot(H[4],H[0],'b--',label='dU50r')
        plt.plot(H[5],H[0],'g-',label='U50m')
        plt.plot(H[6],H[0],'g--',label='dU50m')
        
        xmax=0.
        for i in range(len(H[1])):
            if H[1][i] >= xmax:
                xmax=H[1][i]
        for j in range(len(H[1])):
            if H[2][j] >= xmax:
                xmax=H[2][j]
        for k in range(len(H[1])):
            if H[3][k] >= xmax:
                xmax=H[3][k]
        for l in range(len(H[1])):
            if H[4][l] >= xmax:
                xmax=H[4][l]
        for m in range(len(H[1])):
            if H[5][m] >= xmax:
                xmax=H[5][m]
        for n in range(len(H[1])):
            if H[6][n] >= xmax:
                xmax=H[6][n]
        plt.axis([0.,xmax,-Hmax,0.])
        plt.title('Watersnelheid LC: 1max, 50red, 50max')
        plt.xlabel('U [m/s] / dU [m/s^2]')
        plt.ylabel('Hoogte tov max waterlijn [m]')
        plt.grid(True)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.savefig('Les 2 - Watersnelheden.png',dpi=200,bbox_inches='tight')
        self.H=H
        self.curve_fit()
        plt.close()
        
    def curve_fit(self):
        H=self.H
        x=H[0]
        y1=H[1]
        y2=H[2]
        y3=H[3]
        y4=H[4]
        y5=H[5]
        y6=H[6]
        deg=4
        fit1=np.polyfit(x,y1,deg)
        fit2=np.polyfit(x,y2,deg)
        fit3=np.polyfit(x,y3,deg)
        fit4=np.polyfit(x,y4,deg)
        fit5=np.polyfit(x,y5,deg)
        fit6=np.polyfit(x,y6,deg)
        print('       x bounds [',min(x),max(x),']')
        print('   U1max bounds [',min(y1),max(y1), ']')
        print('  dU1max bounds [',min(y2),max(y2), ']')
        print('  U50red bounds [',min(y3),max(y3), ']')
        print(' dU50red bounds [',min(y4),max(y4), ']')
        print('  U50max bounds [',min(y5),max(y5), ']')
        print(' dU50max bounds [',min(y6),max(y6), ']')
        print('  U1max(x) =', fit1[0], 'x⁴ + ', fit1[1], 'x³ + ',fit1[2], 'x² + ',fit1[3], 'x + ',fit1[4])
        print(' dU1max(x) =', fit2[0], 'x⁴ + ', fit2[1], 'x³ + ',fit2[2], 'x² + ',fit2[3], 'x + ',fit2[4])
        print(' U50red(x) =', fit3[0], 'x⁴ + ', fit3[1], 'x³ + ',fit3[2], 'x² + ',fit3[3], 'x + ',fit3[4])
        print('dU50red(x) =', fit4[0], 'x⁴ + ', fit4[1], 'x³ + ',fit4[2], 'x² + ',fit4[3], 'x + ',fit4[4])
        print(' U50max(x) =', fit5[0], 'x⁴ + ', fit5[1], 'x³ + ',fit5[2], 'x² + ',fit5[3], 'x + ',fit5[4])
        print('dU50max(x) =', fit6[0], 'x⁴ + ', fit6[1], 'x³ + ',fit6[2], 'x² + ',fit6[3], 'x + ',fit6[4])
        
        text=open('Les 2 - Environmental data.txt','a')
        text.truncate(0)
        text.write('Polynomal curve fitting water data per loadcase: '+'\n')
        text.write('\n'+'      x bounds ['+str(min(x))+','+str(max(x))+']'+'\n')
        text.write('  U1max bounds ['+str(min(y1))+','+str(max(y1))+']'+'\n')
        text.write(' dU1max bounds ['+str(min(y2))+','+str(max(y2))+']'+'\n')
        text.write(' U50red bounds ['+str(min(y3))+','+str(max(y3))+']'+'\n')
        text.write('dU50red bounds ['+str(min(y4))+','+str(max(y4))+']'+'\n')
        text.write(' U50max bounds ['+str(min(y5))+','+str(max(y5))+']'+'\n')
        text.write('dU50max bounds ['+str(min(y6))+','+str(max(y6))+']'+'\n')
        
        text.write('  U1max(x) ='+ str(fit1[0])+'x4 + '+ str(fit1[1])+'x3 + '+ str(fit1[2])+'x2 + '+ str(fit1[3])+'x + '+ str(fit1[4])+'\n')
        text.write(' dU1max(x) ='+ str(fit2[0])+'x4 + '+ str(fit2[1])+'x3 + '+ str(fit2[2])+'x2 + '+ str(fit2[3])+'x + '+ str(fit2[4])+'\n')
        text.write(' U50red(x) ='+ str(fit3[0])+'x4 + '+ str(fit3[1])+'x3 + '+ str(fit3[2])+'x2 + '+ str(fit3[3])+'x + '+ str(fit3[4])+'\n')
        text.write('dU50red(x) ='+ str(fit4[0])+'x4 + '+ str(fit4[1])+'x3 + '+ str(fit4[2])+'x2 + '+ str(fit4[3])+'x + '+ str(fit4[4])+'\n')
        text.write(' U50max(x) ='+ str(fit5[0])+'x4 + '+ str(fit5[1])+'x3 + '+ str(fit5[2])+'x2 + '+ str(fit5[3])+'x + '+ str(fit5[4])+'\n')
        text.write('dU50max(x) ='+ str(fit6[0])+'x4 + '+ str(fit6[1])+'x3 + '+ str(fit6[2])+'x2 + '+ str(fit6[3])+'x + '+ str(fit6[4])+'\n')
        text.close()
        
    def bereken(self):
        Hmax=self.max_natte_zone(self.Hdepth,self.Hss50m,self.Hw50m,self.Hstm)
        print(self.Uc1m)
        self.Hmax=Hmax
        self.hydrodynamic_conditions()
        water_data=[[[],[]],[[],[]],[[],[]]]
        max_water_data=[[[],[]],[[],[]],[[],[]]]
        for t in range(3600*24):
            #for z in range(self.Hwater):
            z=0.
            Usnelheid_50max=self.golf_snelheid(t,z,'50max')
            Uacceleratie_50max=self.golf_acceleratie(t,z,'50max')
            Usnelheid_50red=self.golf_snelheid(t,z,'50red')
            Uacceleratie_50red=self.golf_acceleratie(t,z,'50red')
            Usnelheid_1max=self.golf_snelheid(t,z,'1max')
            Uacceleratie_1max=self.golf_acceleratie(t,z,'1max')
            water_data[0][0].append(Usnelheid_1max)
            water_data[0][1].append(Uacceleratie_1max)
            water_data[1][0].append(Usnelheid_50red)
            water_data[1][1].append(Uacceleratie_50red*1.01)
            water_data[2][0].append(Usnelheid_50max)
            water_data[2][1].append(Uacceleratie_50max*1.02)
        print(max(water_data[0][0]),self.current_speed(self.Uc1m,'1max'))
        max_water_data[0][0]=max(water_data[0][0])+self.current_speed(self.Uc1m,'1max')
        max_water_data[0][1]=max(water_data[0][1])
        max_water_data[1][0]=max(water_data[1][0])+self.current_speed(self.Uc1m,'50red')
        max_water_data[1][1]=max(water_data[1][1])
        max_water_data[2][0]=max(water_data[2][0])+self.current_speed(self.Uc1m,'50max')
        max_water_data[2][1]=max(water_data[2][1])
        
        return max_water_data
            
       
def bereken():
    Hdepth = float(input('Waterdiepte? [m] '))
    Hsurge50m = float(input('50jaar max storm surge? [m] '))
    Hwave50m = float(input('50jaar max golfhoogte? [m] '))
    Twave50m = float(input('50jaar max golfperiode? [s] '))
    Htidem = float(input('50 jaar gemiddelde getijden? [m] '))
    Hcurrent1m= float(input('1 jaar max getijden snelheid? [m/s] '))
    wave_berekening=wave(Hdepth,Hsurge50m,Hwave50m,Twave50m,Htidem,Hcurrent1m)
    print(wave_berekening.Uc1m)
    max_water_data=wave_berekening.bereken()
    wave_berekening.current_profile_plot(wave_berekening.Hmax,max_water_data)
    print('Klaar! kijk in de map van dir bestand.')
bereken()