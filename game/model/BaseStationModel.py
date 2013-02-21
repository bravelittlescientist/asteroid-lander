'''
Created on 16/02/2013

@author: Christian Adriano
'''
from game.Constants import *
class BaseStationModel(object):
    '''
    This class holds the data shared between the client (Spaceship) and the GameServer.
    This class is used solely by the Spaceship.
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.fuel = 0#MAX_FUEL_BASE_STATION-1
        self.gameScore = {GOLD:0,
                          COPPER:0,
                          IRON:0}
        self.mineGrid = {GOLD:GOLD_PLOT_TOTAL,
                          COPPER:COPPER_PLOT_TOTAL,
                          IRON:IRON_PLOT_TOTAL}
        self.conqueredPlot = {GOLD:0,
                          COPPER:0,
                          IRON:0}
        
    def setgameScore(self, i, value):
        self.gameScore[i] = value
    
    def setMineGrid(self, i, value):
        self.mineGrid[i] = value
        
    def setFuel(self, value):
        self.fuel= value
        
    def getFuel(self):
        return self.fuel

