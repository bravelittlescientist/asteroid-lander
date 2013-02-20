'''
Created on Feb 18, 2013

@author: vaibhavsaini
'''
from game.Constants import *
from game.model.BaseStationModel import BaseStationModel
from game.model.GameRule import GameRule

class BusinessService(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.baseStation = BaseStationModel()
        self.gameRule = GameRule()
    
    def getGameScore(self):
        return self.baseStation.gameScore
    
    def getGridStatus(self):
        return self.baseStation.mineGrid
    
    def buyFuel(self):
        self.baseStation.gameScore[GOLD] = self.baseStation.gameScore[GOLD]-self.gameRule.buyRate
        self.baseStation.fuel = min(MAX_FUEL_BASE_STATION, self.baseStation.fuel+self.gameRule.fuelPerExchangeUnit)
        return self.baseStation.fuel
    
    def canBuyFuel(self):
        if self.baseStation.fuel == MAX_FUEL_BASE_STATION:
            return (False, "BASE STATION FUEL TANK ALREADY AT MAX CAPACITY" )
        if self.baseStation.gameScore[GOLD]>= self.gameRule.buyRate:
            return (False, "NOT ENOUGH GOLD TO BUY FUEL")
        return ((self.baseStation.fuel < MAX_FUEL_BASE_STATION) and (self.baseStation.gameScore[GOLD]>= self.gameRule.buyRate),"SUCCESS")
    
    def assignPlot(self,type):
        self.baseStation.mineGrid[type] = self.baseStation.mineGrid[type]-1
    def freePlot(self,type):
        self.baseStation.mineGrid[type] = self.baseStation.mineGrid[type]+1
    def canAssignPlot(self,type):
        if self.baseStation.mineGrid[type]<1:
            return (False, "NO MORE PLOTS AVAILABLE OF THIS TYPE")
        return (True,"SUCCESS")
    
    def conquerPlot(self,type):
        if self.baseStation.conqueredPlot[type]< self.gameRule.maxPlotCount[type]:
            self.baseStation.conqueredPlot[type] = self.baseStation.conqueredPlot[type]+1
            
    def updateGameScore(self,data):
        self.baseStation.gameScore[GOLD] += data[GOLD]
        self.baseStation.gameScore[IRON] += data[IRON]
        self.baseStation.gameScore[COPPER] += data[COPPER]
        
    def checkGoalAccomplished(self):
        if self.baseStation.gameScore[GOLD] >= self.gameRule.gameGoal[GOLD] and self.baseStation.gameScore[IRON] >= self.gameRule.gameGoal[IRON] and  self.baseStation.gameScore[COPPER] >= self.gameRule.gameGoal[COPPER]:
            return True
        else: 
            return False
    
    def getBaseStationFuelLevel(self):
        return self.baseStation.getFuel()
        
    def withdrawFuel(self,amountRequested):
        if self.baseStation.getFuel() > amountRequested:
            self.baseStation.setFuel(self.baseStation.getFuel()-amountRequested)
            return amountRequested
        else:
            available = amountRequested-self.baseStation.getFuel()
            self.baseStation.setFuel(0)
            return available
        