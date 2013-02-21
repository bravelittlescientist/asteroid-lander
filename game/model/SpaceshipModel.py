'''
Created on 16/02/2013

@author: Christian Adriano
'''
from game.Constants import *


class SpaceshipModel(object):
    '''
    Keeps all the state variables of the Spaceship
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.active = True
         # update the number of active players
        self.score = 0;
        self.assignedPlot = 0
        self.mass = SPACESHIP_OWN_MASS
        self.cargoCapacity = SPACESHIP_CARGO_CAPACITY
        self.fuelLevel=100
        self.fuelCapacity=100
        self.altitude=1000
        self.minerals = {GOLD:0,
                       COPPER:0,
                       IRON:0}
        
    def setAltitude(self, value):
        self.altitude = value
        
    def getAltitude(self): 
        return self.altitude
    
    def getAvailableCapacity(self):
        used = 0
        for key in self.minerals.keys():
            used += self.minerals[key]
        return self.cargoCapacity - used
    
    def setFuelLevel(self, value):
        self.fuelLevel = value
        
    def getFuelLevel(self): 
        return self.fuelLevel
    
    def getSelfStateObj(self):
        return vars(self)
