'''
Created on 16/02/2013

@author: Christian Adriano
'''

class SpaceshipModel(object):
    '''
    Keeps all the state variables of the Spaceship
    '''

    altitude = 1000

    def __init__(self, selfparams):
        '''
        Constructor
        '''
    def setAltitude(self, value):
        self.altitude = value
        
    def getAltitude(self): return self.altitude
    
    