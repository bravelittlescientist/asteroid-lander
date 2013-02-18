'''
Created on Feb 17, 2013

@author: vaibhavsaini
'''
from Constants import *
class GameRule(object):
    '''
    classdocs
    '''


    def __init__(self,params):
        '''
        Constructor
        '''
        self.buyRate = BUY_RATE
        self.exchangeUnit = GOLD
        self.fuelPerExchangeUnit = FUEL_EXCHANGE
        self.gameGoal = {GOLD:30,
                          COPPER:80,
                          IRON:120}
        self.maxPlotCount = {GOLD:GOLD_PLOT_TOTAL,
                          COPPER:COPPER_PLOT_TOTAL,
                          IRON:IRON_PLOT_TOTAL}
    
    def getBuyRate(self):
        return self.buyRate
    
    def getExchangeUnit(self):
        return self.exchangeUnit
    
    
    