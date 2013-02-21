'''
Created on Feb 17, 2013

@author: vaibhavsaini
'''
from game.Constants import *
class GameRule(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.buyRate = BUY_RATE
        self.exchangeUnit = GOLD
        self.fuelPerExchangeUnit = FUEL_EXCHANGE
        self.gameGoal = {GOLD:30,
                          COPPER:80,
                          IRON:120}
        self.plots = {GOLD:{MINE_LIMIT_STRING:GOLD_MINE_LIMIT,
                             TOTAL_COUNT_STRING:GOLD_PLOT_TOTAL
                             },
                      COPPER:{MINE_LIMIT_STRING:COPPER_MINE_LIMIT,
                              TOTAL_COUNT_STRING:COPPER_PLOT_TOTAL
                              },
                      IRON:{MINE_LIMIT_STRING:IRON_MINE_LIMIT,
                            TOTAL_COUNT_STRING:IRON_PLOT_TOTAL}
                      }
    def getBuyRate(self):
        return self.buyRate
    
    def getExchangeUnit(self):
        return self.exchangeUnit
