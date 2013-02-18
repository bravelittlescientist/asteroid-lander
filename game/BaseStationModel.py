'''
Created on 16/02/2013

@author: Christian Adriano
'''

class BaseStationModel(object):
    '''
    This class holds the data shared between the client (Spaceship) and the GameServer.
    This class is used solely by the Spaceship.
    '''
    fuel = 0
    gameScore = [0,0,0]
    mineGrid = [0,0,0]

    def __init__(self, selfparams):
        '''
        Constructor
        '''
        
    def setgameScore(self, i,value):
        self.gameScore[i] = value
    
    def setMineGrid(self, i,value):
        self.mineGrid[i] = value
        
    def setfuel(self, value):
        self.fuel= value