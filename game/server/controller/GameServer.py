from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from collections import namedtuple
from game.Constants import *
from game.model.SpaceshipModel import SpaceshipModel
from game.server.businessservice.BusinessService import BusinessService
from random import randint
from time import sleep, localtime
from weakref import WeakKeyDictionary
import ServerHelper
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
        a) check the spaceship's available space, and load x units minerals to spaceship based on plot type
        b) increase player's score based on the points, as received from the client
        c) increase the mass of the spaceship by x units 
        d) set the plot conquered
        e) notify that a plot of this plot-type has been conqured
        f) notify to update leaderboard
        g) notify the grid status
        '''
        # add to the score of this client.
        self.spaceship.score += data['points_scored']
        # generate the new leaderboard information
        
        if self.spaceship.assignedPlot !=0:
            self._server.conquerPlot(self.spaceship.assignedPlot)
            self.spaceship.assignedPlot = 0
            self.SendGridStatus()
        self.SendLeaderBoard()
        self.SendNotification("HURRAY!!! Player " + str(self.id)+ " has conqured a "+ data['plot_type']+" plot")
    
    def BuyFuel(self, data):
        return_data = {}
        canBuyFuel = self._server.canBuyFuel()
        if canBuyFuel[0]:
            #buy fuel now
            return_data.update({BASE_STATION_FUEL_UPDATED: self._server.buyFuel()})
            return_data.update({"response_action" : BASE_STATION_FUEL_UPDATED})
            self.PassOn(return_data)
            self.SendNotification("Player " + str(self.id)+ " bought fuel")
            # because gold was spent to buy fuel, we need to update game score
            self.SendGameScore()
        else:
            return_data.update({FUEL_REQUEST_DENIED: canBuyFuel[1]})
            return_data.update({"response_action" : FUEL_REQUEST_DENIED})
            self.send(return_data)
    
    def AssignPlot(self,data):
        '''
        checks if a plot of plot type is  available and if yes, then assign it. 
        '''
        return_data = {}
        canAssignPlot = self._server.canAssignPlot(data)
        if canAssignPlot[0]:
            #assign plot now
            return_data.update({REQUEST_PLOT_APPROVED: self._server.getPlot(data)})
            return_data.update({"response_action" : REQUEST_PLOT_APPROVED})
            self.assignedPlot = data['plot_type']
            self.PassOn(return_data)
            self.SendNotification("Player " + str(self.id)+ " has been assigned a "+ data['plot_type']+" plot" )
            self.SendGridStatus()
        else:
            # plot of this type not available
            return_data.update({REQUEST_PLOT_DENIED: canAssignPlot[1]})
            return_data.update({"response_action" : REQUEST_PLOT_DENIED})
            self.send(return_data)
            # notify the grid status.
            self.SendGridStatus()
    
    def ProcessCrash(self, data):
        # subtracts one player from the game and set the player as inactive
        self.active = False
        self._server.subtractPlayer() 
        new_data ={}
        new_data.update({"response_action":GAME_OVER_FOR_CLIENT})
        #send this new information to all clients, they will just print this on their screens
        self.send(new_data);
        #Now warn all other players that the player crashed.
        self.SendNotification("Player "+self.id+" crashed")
        self._server.freePlot(data)
        self.SendGridStatus()
    
    def ReturnToEarth(self, data):
        '''
        a) check if the spaceship has any mineral.
        '''
    def SendLeaderBoard(self):
        new_data ={}
        new_data.update({PRINT_LEADERBOARD: self._server.getLeaderboard()})
        new_data.update({"response_action":PRINT_LEADERBOARD})
        #send this new information to all clients, they will just print this on their screens
        self.PassOn(new_data)
    
    def SendGameScore(self):
        return_data ={}
        return_data.update({UPDATE_GAME_SCORE:self._server.getGameScore()})
        return_data.update({"response_action":UPDATE_GAME_SCORE})
        self.PassOn(return_data)
        
    def SendNotification(self, msg):
        notification_data={}
        notification_data.update({"response_action":NOTIFICATION})
        notification_data.update({NOTIFICATION:msg})
        #send this to all players
        self.PassOn(notification_data);
    def SendGridStatus(self):
        return_data ={}
        return_data.update({UPDATE_GRID_STATUS:self._server.getGridStatus()})
        return_data.update({"response_action":UPDATE_GRID_STATUS})
        self.PassOn(return_data)
    ##################################
    ### Network specific callbacks ###
    ##################################
    
    def Network_startline(self, data):
        # TODO: Update to data we send to client
        self.lines.append([data['point']])
        self.PassOn(data)
    
    def Network_drawpoint(self, data):
        # TODO: Another update to data we send to client
        print "drawpoint"
        self.lines[-1].append(data['point'])
        self.PassOn(data)
    
    def Network(self, data):
        print "event listed at server side"
        action = data['request_action']
        if action == LANDED_SUCCESSFULLY:
            self.HandleSuccessLanding(data)
        elif action == BUY_FUEL:
            self.BuyFuel(data)
        elif action == RETURN_TO_EARTH:
            self.ReturnToEarth(data)
        elif action == CRASH_LANDED:
            pass
        elif action == REQUEST_PLOT:
            pass
        elif action == QUIT_GAME:
            pass

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
        leaderboard =[]
        PlayerInfo = namedtuple('PlayerInfo','name score')
        
        for p in self.players:
            row = PlayerInfo(name=p.id, score=p.score)
            leaderboard.append(row)
        leaderboard.sort(key=self.getPlayerScore,reverse=True)
        print (self.leaderboardToString(self,leaderboard))
        data = self.leaderboardToString(self,leaderboard)
        return data
    
    def canBuyFuel(self):
        return self.service.canBuyFuel()
    
    def buyFuel(self):
        return self.service.buyFuel()
    
    def getGameScore(self):
        return self.service.getGameScore()
    
    def getGridStatus(self):
        return self.service.getGridStatus()
    
    def canAssignPlot(self,data):
        return self.service.canAssignPlot(data['plot_type'])
    
    def getPlot(self,data):
        self.service.assignPlot(data['plot_type'])
        return self.getGridStatus()
    
    def freePlot(self,data):
        self.service.freePlot(data['plot_type'])
        return self.getGridStatus()
    
    def conquerPlot(self,data):
        return self.service.conquerPlot(data)
    
    def subtractPlayer(self):
        self.ActivePlayers= self.ActivePlayers-1

    def addPlayer(self):
        self.ActivePlayers= self.ActivePlayers+1

# get command line argument of server, port
if len(sys.argv) != 2:
    print "Lunar Lander Usage:", sys.argv[0], "host:port"
    print "e.g.", sys.argv[0], "localhost:31425"
else:
    print "hello world"
    host, port = sys.argv[1].split(":")
    s = LunarLanderServer(localaddr=(host, int(port)))
    s.Launch()