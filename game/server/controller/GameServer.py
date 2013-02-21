from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from ServerHelper import *
from collections import namedtuple
from game.Constants import *
from game.model.SpaceshipModel import SpaceshipModel
from game.server.businessservice.BusinessService import BusinessService
from random import randint
from time import sleep, localtime
from weakref import WeakKeyDictionary
import sys


class ServerChannel(Channel):
    """
    This is the server representation of a single connected client.
    """

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.id = str(self._server.NextId())
        intid = int(self.id)
        self._server.addPlayer()
        self.spaceship = SpaceshipModel()
    
    def PassOn(self, data):
        # pass on what we received to all connected clients
        data.update({"id": self.id})
        self._server.SendToAll(data)
    
    def Close(self):
        self._server.DelPlayer(self)
    
    def HandleSuccessLanding(self, data):
        '''
        a) check the spaceship's available space, and load x units minerals to spaceship based on plot type : done
        b) increase player's score based on the points, as received from the client : done
        c) increase the mass of the spaceship by x units : done
        d) set the plot conquered : done
        e) notify that a plot of this plot-type has been conqured : done
        f) notify to update leaderboard : done
        g) notify the grid status   : done
        e) notify the self player about new spaceship state. 
        '''
        print "inside HandleSucessLanding"
        if self.spaceship.assignedPlot != 0:
            print "ship has landed successfully, lets load minerals and increase it's score"
            self.spaceship.score += data['points_scored']
            # load mineral
            self._server.loadMineral(self.spaceship.assignedPlot, self.spaceship)
            self._server.conquerPlot(self.spaceship.assignedPlot)
            self.SendNotification("HURRAY!!! Player " + str(self.id)+ " has conquered a "+ self.spaceship.assignedPlot+" plot")
            self.spaceship.assignedPlot = 0
            self.SendSpaceShipInfoToSelfPlayer()
            self.SendGridStatus()
            self.SendLeaderBoard()
            
        else:
            print "no plot assigned to spaceship, it can not land. this event should not have been passed by client"
    
    def BuyFuel(self):
        return_data = self.GetReturnData()
        canBuyFuel = self._server.canBuyFuel()
        if canBuyFuel[0]:
            #buy fuel now
            return_data.update({BASE_STATION_FUEL_UPDATED: self._server.buyFuel()})
            return_data.update({"response_action" : BASE_STATION_FUEL_UPDATED})
            self.PassOn(return_data)
            self.SendNotification("Player " + str(self.id) + " bought fuel")
            # because gold was spent to buy fuel, we need to update game score
            self.SendGameScore()
        else:
            return_data.update({FUEL_REQUEST_DENIED: canBuyFuel[1]})
            return_data.update({"response_action" : FUEL_REQUEST_DENIED})
            self.Send(return_data)
    
    def GetReturnData(self):
        return {"action":"response"}
    
    def AssignPlot(self, data):
        '''
        checks if a plot of plot type is  available and if yes, then assign it. 
        '''
        return_data = self.GetReturnData()
        canAssignPlot = self._server.canAssignPlot(data)
        if canAssignPlot[0]:
            #assign plot now
            return_data.update({REQUEST_PLOT_APPROVED: self._server.getPlot(data)})
            return_data.update({"response_action" : REQUEST_PLOT_APPROVED})
            self.spaceship.assignedPlot = data['plot_type']
            self.PassOn(return_data)
            self.SendNotification("Player " + str(self.id) + " has been assigned a " + data['plot_type'] + " plot")
            self.SendGridStatus()
        else:
            # plot of this type not available
            return_data.update({REQUEST_PLOT_DENIED: canAssignPlot[1]})
            return_data.update({"response_action" : REQUEST_PLOT_DENIED})
            self.Send(return_data)
            # notify the grid status.
            self.SendGridStatus()
    
    def ProcessCrash(self, data):
        # subtracts one player from the game and set the player as inactive
        self.active = False
        self._server.subtractPlayer() 
        new_data = self.GetReturnData()
        new_data.update({"response_action":GAME_OVER_FOR_CLIENT})
        #send this new information to all clients, they will just print this on their screens
        self.Send(new_data);
        #Now warn all other players that the player crashed.
        self.SendNotification("Player " + self.id + " crashed")
        self._server.freePlot(data)
        self.SendGridStatus()
    
    def ReturnToEarth(self, data):
        '''
        a) update game score with the minerals collected by the spaceship
        b) check if goal was accomplished.
        c) try to refuel spaceship
        d) notify all players about changes in the Base Station fuel level and Game Score
<<<<<<< HEAD
        '''
        
        self._server.updateGameScore(self.spaceship)
        new_data =self.GetReturnData()
        new_data.update({"response_action":UPDATE_GAME_SCORE})
        self.PassOn(new_data)
=======
        '''      
        self.spaceship.minerals[GOLD] = 0
        self.spaceship.minerals[IRON] = 0
        self.spaceship.minerals[COPPER] = 0
        self._server.updateGameScore(data)
>>>>>>> 676434afb0230b31f79a46a30414e0e23b7ca238
        
        if self._server.checkGoalAccomplished():
            self.SendNotification("Mission Accomplished! Congratulations!")
            new_data =self.GetReturnData()
            new_data.update({"response_action":GAME_GOAL_ACHIEVED})
            self.PassOn(new_data)
        elif self._server.canRefuelSpaceship(data):
            fuelAvailable = self._server.withdrawFuel(data)
            self.spaceship.fuelLevel +=fuelAvailable
            new_data = self.GetReturnData()
            new_data.update({BASE_STATION_FUEL_UPDATED: self._server.getBaseStationFuelLevel()})
            new_data.update({"response_action" : BASE_STATION_FUEL_UPDATED})
            self.PassOn(new_data)
            self.SendNotification("Player " + str(self.id)+ " was refueled at Base Station")
        else:
            #No fuel left, game over for this player
            self.active = False
            self._server.subtractPlayer() 
            new_data =self.GetReturnData()
            new_data.update({"response_action":GAME_OVER_FOR_CLIENT})
            #send this new information to all clients, they will just print this on their screens
            self.Send(new_data);
            self.SendNotification("Player "+self.id+" could no refuel at Base Station :( ")

            self.spaceship.minerals[GOLD] = 0
            self.spaceship.minerals[IRON] = 0
            self.spaceship.minerals[COPPER] = 0
        
    def Quit(self,data):
        '''
        A player has quit 
        '''
        # subtracts one player from the game and set the player as inactive
        self.active = False
        self._server.subtractPlayer() 
        new_data =self.GetReturnData()
        new_data.update({"response_action":GAME_OVER_FOR_CLIENT})
        #send this new information to all clients, they will just print this on their screens
        self.Send(new_data);
        self.SendNotification("Player "+self.id+" quit :( ")
        self._server.freePlot(data)
        self.SendGridStatus()
    
    def SendSpaceShipInfoToSelfPlayer(self):
        print "sending spaceshipinfo to player ", self.id
        new_data = self.GetReturnData()
        new_data.update({UPDATE_SPACESHIP_STATE: self.spaceship.getSelfStateObj()})
        new_data.update({"response_action":UPDATE_SPACESHIP_STATE})
        #send this new information to all clients, they will just print this on their screens
        self.PassOn(new_data)
        
    def SendLeaderBoard(self):
        print "sending leaderboard to all"
        new_data = self.GetReturnData()
        new_data.update({PRINT_LEADERBOARD: self._server.getLeaderboard()})
        new_data.update({"response_action":PRINT_LEADERBOARD})
        #send this new information to all clients, they will just print this on their screens
        self.PassOn(new_data)
    
    def SendGameScore(self):
        print "sending game score to all"
        return_data = self.GetReturnData()
        return_data.update({UPDATE_GAME_SCORE:self._server.getGameScore()})
        return_data.update({"response_action":UPDATE_GAME_SCORE})
        self.PassOn(return_data)
        
    def SendNotification(self, msg):
        print "notifying all ", msg
        notification_data = self.GetReturnData()
        notification_data.update({"response_action":NOTIFICATION})
        notification_data.update({NOTIFICATION:msg})
        #send this to all players
        self.PassOn(notification_data);
    def SendGridStatus(self):
        print "sending grid status to all"
        return_data = self.GetReturnData()
        return_data.update({UPDATE_GRID_STATUS:self._server.getGridStatus()})
        return_data.update({"response_action":UPDATE_GRID_STATUS})
        self.PassOn(return_data)
    ##################################
    ### Network specific callbacks ###
    ##################################
    def Network(self, data):
        pass

    def Network_request(self, data):
        print "inside request action event listed at server side"
        if 'request_action' in data:
            action = data['request_action']
            if action == LANDED_SUCCESSFULLY:
                self.HandleSuccessLanding(data)
            elif action == BUY_FUEL:
                self.BuyFuel()
            elif action == RETURN_TO_EARTH:
                self.ReturnToEarth(data)
            elif action == CRASH_LANDED:
                self.ProcessCrash(data)
            elif action == REQUEST_PLOT:
                self.AssignPlot(data)
            elif action == QUIT_GAME:
                self.Quit(data)

class LunarLanderServer(Server):
    channelClass = ServerChannel
    ActivePlayers = 0

    def __init__(self, *args, **kwargs):
        self.id = 0
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self.service = BusinessService()
        print 'Server launched'
    
    def NextId(self):
        self.id += 1
        return self.id
    
    def Connected(self, channel, addr):
        self.AddPlayer(channel)
    
    def AddPlayer(self, player):
        print "New Player" + str(player.addr)
        self.players[player] = True
        # TODO: PLayer creation and data transmission
        print "add player"
        players = self.GetPLayers()
        print players
        print "get player done"
        print "sending initial"
        player.Send({"action": "initial", "players": players})
        print "sent initial, calling sendPLayers()"
        self.SendPlayers()

    def GetPLayers(self):
        players = []
        for p in self.players:
            playerObj = {"id" :p.id,
                        "spaceship": p.spaceship.getSelfStateObj()
                        } 
            players.append(playerObj)
        return players
    
    def DelPlayer(self, player):
        print "Deleting Player" + str(player.addr)
        del self.players[player]
        self.SendPlayers()
    
    def SendPlayers(self):
        # TODO: Transmit data to players/clients
        players = self.GetPLayers()
        self.SendToAll({"action": "players", "players": players})
    
    def SendToAll(self, data):
        [p.Send(data) for p in self.players]
    
    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)
    def getLeaderboard(self):
        leaderboard = []
        PlayerInfo = namedtuple('PlayerInfo', 'name score')
        
        for p in self.players:
            row = PlayerInfo(name=p.id, score=p.spaceship.score)
            leaderboard.append(row)
        leaderboard.sort(key=self.getPlayerScore, reverse=True)
        print (self.leaderboardToString(leaderboard))
        data = self.leaderboardToString(leaderboard)
        return data
    
    def canBuyFuel(self):
        return self.service.canBuyFuel()
    
    def buyFuel(self):
        return self.service.buyFuel()
    
    def getGameScore(self):
        return self.service.getGameScore()
    
    def getGridStatus(self):
        return self.service.getGridStatus()
    
    def canAssignPlot(self, data):
        return self.service.canAssignPlot(data['plot_type'])
    
    def getPlot(self, data):
        self.service.assignPlot(data['plot_type'])
        return self.getGridStatus()
    
    def freePlot(self, data):
        self.service.freePlot(data['plot_type'])
        return self.getGridStatus()
    
    def conquerPlot(self, data):
        return self.service.conquerPlot(data)
    
    def loadMineral(self, data, spaceship):
        self.service.loadMineral(data, spaceship)
    
    def subtractPlayer(self):
        self.ActivePlayers = self.ActivePlayers - 1

    def addPlayer(self):
        self.ActivePlayers = self.ActivePlayers + 1

    def updateGameScore(self,spaceship):
        return self.service.updateGameScore(spaceship)

    def checkGoalAccomplished(self):
        return self.service.checkGoalAccomplished()
    
    def canRefuelSpaceship(self, data):
        if self.service.getBaseStationFuelLevel()>0:
            return True
        else:
            return False
    def getPlayerScore(self, pInfo):
        return pInfo.score
    
    def playerInfoToString(self,pInfo):
        return str(pInfo.name) + "  :  " + str(pInfo.score)
    
    def leaderboardToString(self, leaderboard):
        returnString = "player  :   score"
        returnString += "*"*10
        for pInfo in leaderboard:
            returnString += "\n" + self.playerInfoToString(pInfo)
        returnString += "\n" + "*"*10
        return returnString

    def withdrawFuel(self,data):
        spaceshipFuelLevel = data[SPACESHIP_FUEL_KEY]
        return self.service.withdrawFuel(SPACESHIP_FUEL_CAPACITY-spaceshipFuelLevel)
        
    def getBaseStationFuelLevel(self):
        return self.service.getBaseStationFuelLevel()

# get command line argument of server, port
if len(sys.argv) != 2:
    print "Lunar Lander Usage:", sys.argv[0], "host:port"
    print "e.g.", sys.argv[0], "localhost:31425"
else:
    print "hello world"
    host, port = sys.argv[1].split(":")
    s = LunarLanderServer(localaddr=(host, int(port)))
    s.Launch()
