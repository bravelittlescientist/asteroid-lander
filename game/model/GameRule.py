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
        self.gameGoal = {GOLD:20,
                          COPPER:0,
                          IRON:0}
        self.plots = {GOLD:{'mine_limit':GOLD_MINE_LIMIT,
                             'total_count':GOLD_PLOT_TOTAL
                             },
                      COPPER:{'mine_limit':COPPER_MINE_LIMIT,
                              'total_count':COPPER_PLOT_TOTAL
                              },
                      IRON:{'mine_limit':IRON_MINE_LIMIT,
                            'total_count':IRON_PLOT_TOTAL}
                      }
    def getBuyRate(self):
        return self.buyRate
    
    def getExchangeUnit(self):
        return self.exchangeUnit
