'''
Created on 16/02/2013

@author: Christian Adriano
'''
from game.Constants import *


class SpaceshipModel(object):
    '''
    Keeps all the state variables of the Spaceship
    '''

    altitude = 1000

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
        self.minerals = {GOLD:0,
                       COPPER:0,
                       IRON:0}
        
    def setAltitude(self, value):
        self.altitude = value
        
    def getAltitude(self): 
        return self.altitude
    
    def GetAvailableCapacity(self):
        used = 0
        for key in self.minerals.keys():
            used += self.minerals[key]
        return self.cargoCapacity - used
    
    def getSelfStateObj(self):
        return vars(self)
