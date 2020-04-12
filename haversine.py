'''
    File Name:      haversine.py
    Description:    Using the haversine algorithm, it returns the current distance from the lat-long (received as an argument)
    Author:         Nirav Jasani
    Date:           Version 1.0 
                    (February 24 -2020):
                    -Working good manually. (By passing lat-long manually)
                    
                    (March 5 2020):
                    -Working as expected with GPS module 
                

'''


#########################Importing modules#######################

from __future__ import division
from math import atan2,cos,radians,sin,sqrt
import time

###############################class##############################
class Haversine:
    '''
    Predefined hazardous areas locations from database
    '''
    HomerBlock=[43.418409, -80.470779]    #Homer watson Blvd and Block Line Rd iuntersection
    FairwayWilson=[43.421105, -80.442763] #Fairway Rd and Wilson Ave intersection
    HasplarBishop=[43.395288, -80.323960] #Hasplar Road and Bishop Street Intersection
    HasplarMaple=[43.435020, -80.327608]  #Hasplar Road and Maple Grove Rd/Fisher Mills Rd
    HasplarQueen=[43.420036, -80.328718]  #Hasplar ROad and Beaverdale Rd/ Queen St
    
    def __init__(self,c1,c2):
        '''
        implementing Haversine algorithm to find linear distance
        '''

        lat1,long1=c1
        lat2,long2=c2

        radious=6371000 #earth radious
        p1=radians(lat1)
        p2=radians(lat2)

        delta_p=radians(lat2-lat1)
        delta_l=radians(long2-long1)
        '''
            Haversine algorithm implementation
        '''
        x=(sin(delta_p/2.0)**2 + cos(p1)*cos(p2) * sin(delta_l/2.0)**2)
        y=2*atan2(sqrt(x),sqrt(1-x))

        self.radious=radious
        self.y=y

    '''
        Returning current distance in various measurement UNIT
    '''
    def m(self): # in mtr
        return self.radious*self.y
    def km(self): #in Km
        return self.m()/1000.0
    def mi(self): # in Mile
        return self.m() * 0.000621371
    def nm(self): # in nm
        return self.m() *(6080.20 /5280.0)
    def yd(self): # in yard
        return self.m() * 1.0936132983
    def ft(self): # in foot
        return self.mi() * 5280.0

