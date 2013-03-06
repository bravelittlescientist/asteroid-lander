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
        self.baseStation.gameScore[GOLD] = self.baseStation.gameScore[GOLD] - self.gameRule.buyRate
        self.baseStation.fuel = min(MAX_FUEL_BASE_STATION, self.baseStation.fuel + self.gameRule.fuelPerExchangeUnit)
        return self.baseStation.fuel
    
    def canBuyFuel(self):
        if self.baseStation.fuel == MAX_FUEL_BASE_STATION:
            return (False, "BASE STATION FUEL TANK ALREADY AT MAX CAPACITY")
        if self.baseStation.gameScore[GOLD] < self.gameRule.buyRate:
            return (False, "NOT ENOUGH GOLD TO BUY FUEL")
        return (True, "SUCCESS")
    
    def assignPlot(self, type):
        self.baseStation.mineGrid[type] = self.baseStation.mineGrid[type] - 1
        
    def freePlot(self,type):
        if type==GOLD or type==IRON or type==COPPER:
            self.baseStation.mineGrid[type] = self.baseStation.mineGrid[type] + 1
            
    def canAssignPlot(self, type, spaceship):
        if spaceship.assignedPlot==0:
            if spaceship.getAvailableCapacity()>0:
                if self.baseStation.mineGrid[type] < 1:
                    return (False, "NO MORE PLOTS AVAILABLE OF THIS TYPE")
                else:
                    return (True, "SUCCESS")
            else:
                return (False, "You Must return to Earth to unload your cargo. You have reached max capacity".upper())
        else:
            return (False, "ALREADY ASSIGNED A PLOT. DON'T BE GREEDY LAND ON ONE PLOT AT A TIME ;)")

    def conquerPlot(self,type):
        if self.baseStation.conqueredPlot[type]< self.gameRule.plots[type][TOTAL_COUNT_STRING]:
            self.baseStation.conqueredPlot[type] = self.baseStation.conqueredPlot[type]+1

    def loadMineral(self, type, spaceship):
        capacity = spaceship.getAvailableCapacity()
        spaceship.minerals[type] += min(capacity,self.gameRule.plots[type][MINE_LIMIT_STRING])
        spaceship.mass += min(capacity,self.gameRule.plots[type][MINE_LIMIT_STRING])
        return capacity>0
    
    def updateGameScore(self,spaceship):
        self.baseStation.gameScore[GOLD] += spaceship.minerals[GOLD]
        self.baseStation.gameScore[IRON] += spaceship.minerals[IRON]
        self.baseStation.gameScore[COPPER] += spaceship.minerals[COPPER]
        
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
        
