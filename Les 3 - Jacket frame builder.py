# -*- coding: utf-8 -*-
"""
Created on Fri May 25 14:17:02 2018

@author: johan
"""

from math import pi,cos, atan, radians,degrees,sqrt,sin

class wireframe_builder:
    def __init__(self,Dtower,Hinterface,Hdepth):
        self.Dtower=Dtower
        self.Hinterface=Hinterface
        self.Hdepth=Hdepth
        self.Hjacket=abs(Hinterface)
        self.batter=0.08 #predescribed batter old batter was 0.06 from rule of thumb
        self.Dspace=2.0
        
    def printlist(self,wireframe):
        print()
        print('wireframe[i]=     Datalist per bay')
        print('wireframe[i][0]=  number of bays in foundation structure')
        print('wireframe[i][1]=  height of respective bay i')
        print('wireframe[i][2]=  angle of the respective bay brace')
        print('wireframe[i][3]=  top width of the respective bay')
        print('wireframe[i][4]=  bottom width of the respective bay')
        print('wireframe[i][5]=  length diagonal brace')
        print('wireframe[i][6]=  height of bottom bay element from mudline')
        print('wireframe[i][7]=  Left top leg angle')
        print('wireframe[i][8]=  Left top brace angle')
        print('wireframe[i][9]=  Right top leg angle')
        print('wireframe[i][10]= Right top brace angle')
        print('wireframe[i][11]= Left bottom leg angle')
        print('wireframe[i][12]= Left bottom brace angle')
        print('wireframe[i][13]= Right bottom leg angle')
        print('wireframe[i][14]= Right bottom brace angle')
        print('wireframe[i][15]= Bay batter')
        
        for bay in range(len(wireframe)):
            print('bay',bay+1,wireframe[bay])
            
        text=open('Les 3 - Data-Jacket.txt','a')
        text.truncate(0)
        text.write('\n'+'wireframe[i]=     Datalist per bay'+'\n')
        text.write('wireframe[i][0]=  number of bays in foundation structure'+'\n')
        text.write('wireframe[i][1]=  height of respective bay i'+'\n')
        text.write('wireframe[i][2]=  angle of the respective bay brace'+'\n')
        text.write('wireframe[i][3]=  top width of the respective bay'+'\n')
        text.write('wireframe[i][4]=  bottom width of the respective bay'+'\n')
        text.write('wireframe[i][5]=  length diagonal brace'+'\n')
        text.write('wireframe[i][6]=  height of bottom bay element from mudline'+'\n')
        text.write('wireframe[i][7]=  Left top leg angle'+'\n')
        text.write('wireframe[i][8]=  Left top brace angle'+'\n')
        text.write('wireframe[i][9]=  Right top leg angle'+'\n')
        text.write('wireframe[i][10]= Right top brace angle'+'\n')
        text.write('wireframe[i][11]= Left bottom leg angle'+'\n')
        text.write('wireframe[i][12]= Left bottom brace angle'+'\n')
        text.write('wireframe[i][13]= Right bottom leg angle'+'\n')
        text.write('wireframe[i][14]= Right bottom brace angle'+'\n')
        text.write('wireframe[i][15]= Bay batter'+'\n')
        
        for bay in range(len(wireframe)):
            text.write('bay '+str(bay+1)+'. 0  Nr of bays: '+str(wireframe[bay][0])+'\n')
            text.write('bay '+str(bay+1)+'. 1  Height bay i: '+str(wireframe[bay][1])+'\n')
            text.write('bay '+str(bay+1)+'. 2  Angle of the respective bay brace: '+str(round(wireframe[bay][2],1))+'\n')
            text.write('bay '+str(bay+1)+'. 3  Top width of the respective bay: '+str(round(wireframe[bay][3],1))+'\n')
            text.write('bay '+str(bay+1)+'. 4  Bottom width of the respective bay: '+str(round(wireframe[bay][4],1))+'\n')
            text.write('bay '+str(bay+1)+'. 5  Length diagonal brace: '+str(round(wireframe[bay][5],1))+'\n')
            text.write('bay '+str(bay+1)+'. 6  Height of bottom bay element from mudline: '+str(round(wireframe[bay][6],1))+'\n')
            text.write('bay '+str(bay+1)+'. 7  Left top leg angle: '+str(round(wireframe[bay][7],1))+'\n')
            text.write('bay '+str(bay+1)+'. 8  Left top brace angle: '+str(round(wireframe[bay][8],1))+'\n')
            text.write('bay '+str(bay+1)+'. 9  Right top leg angle: '+str(round(wireframe[bay][9],1))+'\n')
            text.write('bay '+str(bay+1)+'. 10 Right top brace angle: '+str(round(wireframe[bay][10],1))+'\n')
            text.write('bay '+str(bay+1)+'. 11 Left bottom leg angle: '+str(round(wireframe[bay][11],1))+'\n')
            text.write('bay '+str(bay+1)+'. 12 Left bottom brace angle: '+str(round(wireframe[bay][12],1))+'\n')
            text.write('bay '+str(bay+1)+'. 13 Right bottom leg angle: '+str(round(wireframe[bay][13],1))+'\n')
            text.write('bay '+str(bay+1)+'. 14 Right bottom brace angle: '+str(round(wireframe[bay][14],1))+'\n')
            text.write('bay '+str(bay+1)+'. 15 Bay batter: '+str(wireframe[bay][15])+'\n')
        text.close()
        
    def bracelength(self,Ltop,Lbottom,angle):
        Lhoriz=Ltop+abs(Ltop-Lbottom)/2.
        Ldiag=Lhoriz*cos(angle*pi/180.)
        return Ldiag
        
    def build(self):
        Ltop=2*self.Dspace+self.Dtower
        Lbottom=Ltop+2.0*self.batter*self.Hjacket
        maxbay=20
        datalist=[]
        difflist=[]
        for i in range(maxbay):
            datalist.append([])
            
        for i in range(maxbay):
            #Calculate different bay configurations
            bay=i+1
            Hbay=1.0*self.Hjacket/bay
            for j in range(bay):
                #Calculate dimensions of each bay
                Lbottom=Ltop+2*self.batter*Hbay
                Ltriangle=Lbottom-self.batter*Hbay
                angle=atan(Hbay/Ltriangle)*180/pi
                datalist[i].append([bay,Hbay,angle,Ltop,Lbottom])
                Ltop=Lbottom
      
        for i in range(maxbay):
            #now we compare which configuration has the top brace angle closest to 45 degrees
            bay=i+1
            mean=45.0*bay
            offset=0
            for j in range(bay):
                offset=offset+datalist[i][0][2] #here the zero looks only at the top brace angle
            difflist.append(mean-offset)
        difference=min(difflist,key=abs)
        for i in range(len(difflist)):
            difflist[i]=difflist[i]/difference

        configNR=difflist.index(1)
        wireframe=datalist[configNR]
        
        for i in range(wireframe[0][0]):
            wireframe[i].append(self.bracelength(wireframe[i][3],wireframe[i][4],wireframe[i][2]))
            wireframe[i].append((wireframe[i][0]-(i+1))*wireframe[i][1])
            
        #Finally we calculate member angles for future calculations
        for bay in range(wireframe[0][0]):
            batterangle=atan(2*wireframe[bay][1]/(wireframe[bay][4]-wireframe[bay][3]))
            #First for the top of the bay
            #       We have the following case                              + (vertical positive direction)
            #       ------------                    /  rotation positive    /\
            #      /\ A      B /\                  / ) +  direction         |
            #     / \brace    / \ leg             ------- angle = 0 RAD     |------> + (horizontal positive direction)
            # We calculate all the angles with respect to the nearest horizontal member with positive direction against the clock.
            philegA=pi+batterangle
            phibraceA=2*pi-radians(wireframe[bay][2])
            philegB=2*pi-batterangle
            phibraceB=pi+radians(wireframe[bay][2])
            wireframe[bay].append(degrees(philegA))
            wireframe[bay].append(degrees(phibraceA))
            wireframe[bay].append(degrees(philegB))
            wireframe[bay].append(degrees(phibraceB))
            
            #First we take a look at everything above the new horizontal bracelime of bottom of the bay
            #     | /               \ |
            #     |/ C            D \ |
            #     - - - - - - - - - - - (Horizontal raferece line (is no actual brace))
            philegC=batterangle
            phibraceC=radians(wireframe[bay][2])
            philegD=pi-batterangle
            phibraceD=pi-radians(wireframe[bay][2])
            wireframe[bay].append(degrees(philegC))
            wireframe[bay].append(degrees(phibraceC))
            wireframe[bay].append(degrees(philegD))
            wireframe[bay].append(degrees(phibraceD))
            wireframe[bay].append(self.batter)
            
        return wireframe
        
class Jacket:
    def __init__(self):
        self.wireframe=[]
        self.dimensions=[]
        self.equivalent_diameter_list=[]
        
    def prelim_geometry_jacket(self,wireframe):
        Guessed_dimension_list=[]
        for baynumber in range(len(wireframe)):
            Dleg=1.0
            Dbrace=Dleg*0.6
            
            wtleg=Dleg/20.
            wtbrace=Dbrace/20.
            Aleg=pi/4.*(Dleg**2-(Dleg-2*wtleg)**2)
            Abrace=pi/4.*(Dbrace**2-(Dbrace-2*wtbrace)**2)
            Guessed_dimension_list.append([Dleg,Dbrace,wtleg,wtbrace,Aleg,Abrace])
        self.dimensions=Guessed_dimension_list
        
    def geometry_jacket(self,wireframe):
        Dimension_list=[]
        for baynumber in range(len(wireframe)):
            if baynumber == 0:
                print('Bay 1 (bovenaan): ')
            else:
                print('Bay ',baynumber+1, ': ')
            Dleg=float(input('Diameter van leg [m] ? : '))
            Dbrace=float(input('Diameter van brace [m] ? : '))
            wtleg=float(input('wanddikte van leg [m] ? : '))
            wtbrace=float(input('wanddikte van brace [m] ? : '))
            Aleg=pi/4.*(Dleg**2-(Dleg-2*wtleg)**2)
            Abrace=pi/4.*(Dbrace**2-(Dbrace-2*wtbrace)**2)
            Dimension_list.append([Dleg,Dbrace,wtleg,wtbrace,Aleg,Abrace])
        self.dimensions=Dimension_list
        
    def mass_jacket_per_bay(self,dimensions_list,wireframe):
        for bay in range(len(wireframe)):
            Aleg=dimensions_list[bay][4]
            Lleg=wireframe[bay][1]*(1.+wireframe[bay][15])
            Abrace=dimensions_list[bay][4]
            Lbrace=wireframe[bay][5]
            Vbay=4.*Aleg*Lleg+8*Abrace*Lbrace
            dimensions_list[bay].append(Vbay*8000./1000.)
        self.dimensions=dimensions_list
        
    def printlist_guessD(self,Guessed_dimensions):
        print()
        print('Dimensions[i]=    Datalist per bay containing user given dimensions')
        print('Dimensions[i][0]= Dleg [m]')
        print('Dimensions[i][1]= Dbrace [m]')
        print('Dimensions[i][2]= wtleg [m]')
        print('Dimensions[i][3]= wtbrace [m]')
        print('Dimensions[i][4]= Aleg [m2]')
        print('Dimensions[i][5]= Abrace [m2]')
        print('Dimensions[i][6]= Mbay [t] ')
        for bay in range(len(Guessed_dimensions)):
            print('bay',bay+1,Guessed_dimensions[bay])
        
        text=open('Les 3 - Data-Jacket.txt','a')
        text.write('\n'+'Guessed Dimensions[i]=    Datalist per bay containing initial quess dimensions'+'\n')
        text.write('Dimensions[i][0]= Dleg [m]'+'\n')
        text.write('Dimensions[i][1]= Dbrace [m]'+'\n')
        text.write('Dimensions[i][2]= wtleg [m]'+'\n')
        text.write('Dimensions[i][3]= wtbrace [m]'+'\n')
        text.write('Dimensions[i][4]= Aleg [m2]'+'\n')
        text.write('Dimensions[i][5]= Abrace [m2]'+'\n')
        text.write('Dimensions[i][6]= Mbay [t]'+'\n')
        for bay in range(len(Guessed_dimensions)):
            text.write('bay '+str(bay+1)+' Dleg [m]     : '+str(Guessed_dimensions[bay][0])+'\n')
            text.write('bay '+str(bay+1)+' Dbrace [m]   : '+str(Guessed_dimensions[bay][1])+'\n')
            text.write('bay '+str(bay+1)+' wtleg [m]    : '+str(Guessed_dimensions[bay][2])+'\n')
            text.write('bay '+str(bay+1)+' wtbrace [m]  : '+str(Guessed_dimensions[bay][3])+'\n')
            text.write('bay '+str(bay+1)+' Aleg [cm2]   : '+str(int(Guessed_dimensions[bay][4]*100*100))+'\n')
            text.write('bay '+str(bay+1)+' Abrace [cm2] : '+str(int(Guessed_dimensions[bay][5]*100*100))+'\n')
            text.write('bay '+str(bay+1)+' Mbay [t]     : '+str(int(Guessed_dimensions[bay][6]))+'\n')
        text.close()
        
    def printlist_D(self,Dimensions):
        print()
        print('Dimensions[i]=    Datalist per bay containing user given dimensions')
        print('Dimensions[i][0]= Dleg [m]')
        print('Dimensions[i][1]= Dbrace [m]')
        print('Dimensions[i][2]= wtleg [m]')
        print('Dimensions[i][3]= wtbrace [m]')
        print('Dimensions[i][4]= Aleg [m2]')
        print('Dimensions[i][5]= Abrace [m2]')
        print('Dimensions[i][6]= Mbay [t] ')
        for bay in range(len(Dimensions)):
            print('bay',bay+1,Dimensions[bay])
        
        text=open('Les 3 - Data-Jacket.txt','a')
        text.write('\n'+'Dimensions[i]=    Datalist per bay containing user given dimensions'+'\n')
        text.write('Dimensions[i][0]= Dleg [m]'+'\n')
        text.write('Dimensions[i][1]= Dbrace [m]'+'\n')
        text.write('Dimensions[i][2]= wtleg [m]'+'\n')
        text.write('Dimensions[i][3]= wtbrace [m]'+'\n')
        text.write('Dimensions[i][4]= Aleg [m2]'+'\n')
        text.write('Dimensions[i][5]= Abrace [m2]'+'\n')
        text.write('Dimensions[i][6]= Mbay [t]'+'\n')
        for bay in range(len(Dimensions)):
            text.write('bay '+str(bay+1)+' Dleg [m]     : '+str(round(Dimensions[bay][0],2))+'\n')
            text.write('bay '+str(bay+1)+' Dbrace [m]   : '+str(round(Dimensions[bay][1],2))+'\n')
            text.write('bay '+str(bay+1)+' wtleg [m]    : '+str(round(Dimensions[bay][2],2))+'\n')
            text.write('bay '+str(bay+1)+' wtbrace [m]  : '+str(round(Dimensions[bay][3],2))+'\n')
            text.write('bay '+str(bay+1)+' Aleg [cm2]   : '+str(int(Dimensions[bay][4]*100*100))+'\n')
            text.write('bay '+str(bay+1)+' Abrace [cm2] : '+str(int(Dimensions[bay][5]*100*100))+'\n')
            text.write('bay '+str(bay+1)+' Mbay [t]     : '+str(int(Dimensions[bay][6]))+'\n')
        text.close()
        
    def printlist_eqD(self,Equivalent_diameter):
        print('For calculation of morison loads (drag+inertia loads):')
        print('Equivalent diameter[i]=          Datalist per bay')
        print('Equivalent diameter[i][0]=       Equivalent drag for 0 degree inflow')
        print('Equivalent diameter[i][1]=       Equivalent drag for 45 degree inflow')
        print('Equivalent diameter[i][2]=       Equivalent inertia for 0 degree inflow')
        print('Equivalent diameter[i][3]=       Equivalent inertia for 45 degree inflow')
        for bay in range(len(Equivalent_diameter)):
            print('bay',bay+1,Equivalent_diameter[bay])
            
        text=open('Les 3 - Data-Jacket.txt','a')
        text.write('\n'+'For calculation of morison loads (drag+inertia loads):''\n')
        text.write('Equivalent diameter[i]=          Datalist per bay'+'\n')
        text.write('Equivalent diameter[i][0]=       Equivalent drag for 0 degree inflow'+'\n')
        text.write('Equivalent diameter[i][1]=       Equivalent drag for 45 degree inflow'+'\n')
        text.write('Equivalent diameter[i][2]=       Equivalent inertia for 0 degree inflow'+'\n')
        text.write('Equivalent diameter[i][3]=       Equivalent inertia for 45 degree inflow'+'\n')
        for bay in range(len(Equivalent_diameter)):
            text.write('bay '+str(bay+1)+' Equivalent drag for 0 degree inflow [m]:     '+str(round(Equivalent_diameter[bay][0],2))+'\n')
            text.write('bay '+str(bay+1)+' Equivalent drag for 45 degree inflow [m]:    '+str(round(Equivalent_diameter[bay][1],2))+'\n')
            text.write('bay '+str(bay+1)+' Equivalent inertia for 0 degree inflow [m]:  '+str(round(Equivalent_diameter[bay][2],2))+'\n')
            text.write('bay '+str(bay+1)+' Equivalent inertia for 45 degree inflow [m]: '+str(round(Equivalent_diameter[bay][3],2))+'\n')
        text.close()
        
    def equivalent_diameter_builder(self,Dimensions):
        equivalent_diameter=[]
        
        for baynumber in range(len(Dimensions)):
            Ddrag0,Ddrag45,Dinertia0,Dinertia45=self.baycalculator(baynumber,Dimensions)
            equivalent_diameter.append([Ddrag0,Ddrag45,Dinertia0,Dinertia45])
            
        self.equivalent_diameter_list=equivalent_diameter
            
    def baycalculator(self,baynumber,Dimensions):
        #Calculated drag and inertia equivalent for a single bay
        #Baynumber counts from 0 as top
        #input: D,L,angle,wavedirection,configuration,allignment
        Ddrag0=0.0
        Ddrag45=0.0
        Dinertia0=0.0
        Dinertia45=0.0
        for i in range(4):
            #Calculate equivalent diameter of vertical bay piles (4) for 0 and 45 degrees
            Ddrag0=Ddrag0+self.equivalentDRAG(Dimensions[baynumber][0],0,0,0,'vertical',0)
            Ddrag45=Ddrag45+self.equivalentDRAG(Dimensions[baynumber][0],0,0,45,'vertical',0)
            Dinertia0=Dinertia0+(self.equivalentINERTIA(Dimensions[baynumber][0],0,0,0,'vertical',0))**2
            Dinertia45=Dinertia45+(self.equivalentINERTIA(Dimensions[baynumber][0],0,0,45,'vertical',0))**2
            #Caculate equivalent diameter for (diagonal) braces (4) for 0 degrees and perpendicular to waves
        for i in range(4):
            Ddrag0=Ddrag0+self.equivalentDRAG(Dimensions[baynumber][1],self.wireframe[baynumber][5],self.wireframe[baynumber][2],0,'diagonal','perpendicular')
            Dinertia0=Dinertia0+(self.equivalentINERTIA(Dimensions[baynumber][1],self.wireframe[baynumber][5],self.wireframe[baynumber][2],0,'diagonal','perpendicular'))**2
            #Calculate equivalent diameter for (diagonal) braces (4) for 0 degrees and parallel to waves
        for i in range(4):
            Ddrag0=Ddrag0+self.equivalentDRAG(Dimensions[baynumber][1],self.wireframe[baynumber][5],self.wireframe[baynumber][2],0,'diagonal','parallel')
            Dinertia0=Dinertia0+(self.equivalentINERTIA(Dimensions[baynumber][1],self.wireframe[baynumber][5],self.wireframe[baynumber][2],0,'diagonal','parallel'))**2
            #Caculate equivalent diameter for (diagonal) braces (8) for 45 degrees
        for i in range(8):
            Ddrag45=Ddrag45+self.equivalentDRAG(Dimensions[baynumber][1],self.wireframe[baynumber][5],self.wireframe[baynumber][2],45,'diagonal',0)
            Dinertia45=Dinertia45+(self.equivalentINERTIA(Dimensions[baynumber][1],self.wireframe[baynumber][5],self.wireframe[baynumber][2],45,'diagonal',0))**2
            #print '8 Diagonal braces 45:',Dinertia45
        Dinertia0=sqrt(Dinertia0)        
        Dinertia45=sqrt(Dinertia45)   
        
        return Ddrag0,Ddrag45,Dinertia0,Dinertia45
            
    def equivalentDRAG(self,D,L,angle,wavedirection,configuration,allignment):
        phi=radians(angle)
        if wavedirection == 0:
            if configuration == 'vertical':
                return D
            elif configuration == 'horizontal':
                if allignment == 'parallel':
                    return 0.0
                elif allignment == 'perpendicular':
                    return L
            elif configuration == 'diagonal':
                if allignment == 'parallel':
                    return D
                elif allignment == 'perpendicular':
                    return D/sin(phi)
        elif wavedirection == 45:
            if configuration == 'vertical':
                return D
            elif configuration == 'horizontal':
                return 1.22*0.5*L
            elif configuration == 'diagonal':
                return 1.22*(0.5*D+D/sin(phi))
        
    def equivalentINERTIA(self,D,L,angle,wavedirection,configuration,allignment):
        phi=radians(angle)
        if wavedirection == 0:
            if configuration == 'vertical':
                return D
            elif configuration == 'horizontal':
                if allignment == 'parallel':
                    return 0.0
                elif allignment == 'perpendicular':
                    return sqrt(D*L)
            elif configuration == 'diagonal':
                if allignment == 'parallel':
                    return D
                elif allignment == 'perpendicular':
                    return D/sqrt(sin(phi))
        elif wavedirection == 45:
            if configuration == 'vertical':
                return D
            elif configuration == 'horizontal':
                return 1.11*0.5*sqrt(D*L)
            elif configuration == 'diagonal':
                return 1.11*(0.5*D+0.5*D/(sqrt(sin(phi))))
                
    def bereken_jacket_prelim(self,Dtower,Hinterface):
        wireframe=wireframe_builder(Dtower,Hinterface,0.)
        self.wireframe=wireframe.build()
        wireframe.printlist(self.wireframe)
        automation=input('Wil je zelf de diameter en wanddiktes van de legs en braces opgeven? [yes/no] ')
        if automation == 'yes':
            self.geometry_jacket(self.wireframe)
        else:
            self.prelim_geometry_jacket(self.wireframe)
        self.mass_jacket_per_bay(self.dimensions,self.wireframe)
        self.equivalent_diameter_builder(self.dimensions)
        self.printlist_guessD(self.dimensions)
        self.printlist_eqD(self.equivalent_diameter_list)
        h=0.
        for bay in range(len(self.wireframe)):
            h=h+self.wireframe[bay][1]
        
def main():
    Dtower=float(input('Wat is de bodem diameter van de toren [m] ? '))
    Hinterface=float(input('Wat is de hoogte van het interface level tov de Mudline [m] ? '))
    Hmsl=0. #float(input('Wat is de hoogte van de MSL tov de Mudline [m] ? '))
    wireframe=wireframe_builder(Dtower,Hinterface,Hmsl)
    frame=wireframe.build()
    wireframe.printlist(frame)
    jacket_berekening=Jacket()
    jacket_berekening.bereken_jacket_prelim(Dtower,Hinterface)
    
main()