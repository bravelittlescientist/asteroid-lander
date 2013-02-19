'''
Created on 16/02/2013

@author: Christian Adriano
'''
from Constants import *
from game import GameRule
class BaseStationModel(object):
    '''
    This class holds the data shared between the client (Spaceship) and the GameServer.
    This class is used solely by the Spaceship.
    '''
    

    def __init__(self, selfparams):
        '''
        Constructor
        '''
        self.fuel = MAX_FUEL_BASE_STATION
        self.gameScore = {GOLD:0,
                          COPPER:0,
                          IRON:0}
        self.mineGrid = {GOLD:GOLD_PLOT_TOTAL,
                          COPPER:COPPER_PLOT_TOTAL,
                          IRON:IRON_PLOT_TOTAL}
        self.conquredPlot = {GOLD:0,
                          COPPER:0,
                          IRON:0}
        
        
        self.gameRule = GameRule()
        
    def setgameScore(self, i,value):
        self.gameScore[i] = value
    
    def setMineGrid(self, i,value):
        self.mineGrid[i] = value
        
    def setfuel(self, value):
        self.fuel= value
        
    def buyFuel(self):
        self.gameScore[GOLD] = self.gameScore[GOLD]-self.gameRule.buyRate
        self.fuel = min(MAX_FUEL_BASE_STATION, self.fuel+self.gameRule.fuelPerExchangeUnit)
    
    def canBuyFuel(self):
        if self.fuel == MAX_FUEL_BASE_STATION:
            return (False, "BASE STATION FUEL TANK ALREADY AT MAX CAPACITY" )
        if self.gameScore[GOLD]>= self.gameRule.buyRate:
            return (False, "NOT ENOUGH GOLD TO BUY FUEL")
        return ((self.fuel < MAX_FUEL_BASE_STATION) and (self.gameScore[GOLD]>= self.gameRule.buyRate),"SUCCESS")
    
    def assignPlot(self,type):
        self.mineGrid[type] = self.mineGrid[type]-1
        
    def freePlot(self,type):
        self.mineGrid[type] = self.mineGrid[type]+1
    
    def canAssignPlot(self,type):
        if self.mineGrid[type]<1:
            return (False, "NO MORE PLOTS AVAILABLE OF THIS TYPE")
        return (True,"SUCCESS")
    
    def conquerPlot(self,type):
        if self.conqueredPlot[type]< self.gameRule.maxPlotCount[type]:
            self.conquredPlot[type] = self.conquredPlot[type]+1
            #TODO: add other things here like what happens when a plot gets conqured.
    
        