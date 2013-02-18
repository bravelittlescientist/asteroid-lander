import sys
from time import sleep, localtime
from random import randint
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
import ServerHelper
from game.Constants import *
from collections import namedtuple

class ServerChannel(Channel):
    """
    This is the server representation of a single connected client.
    """

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.id = str(self._server.NextId())
        intid = int(self.id)

        # TODO: Placeholder for initializing data we send to client
        self.color = [(intid + 1) % 3 * 84, (intid + 2) % 3 * 84, (intid + 3) % 3 * 84] #tuple([randint(0, 127) for r in range(3)])
        self.lines = []
        self.score = 0;
    
    def PassOn(self, data):
        # pass on what we received to all connected clients
        data.update({"id": self.id})
        self._server.SendToAll(data)
    
    def Close(self):
        self._server.DelPlayer(self)
    
    def AddToSelfScore(self, data):
        # add to the score of this client.
        self.score += data['points_scored']
        # generate the new leaderboard information
        new_data ={}
        new_data.update({"print_leaderboard": self._server.getLeaderboard()})
        new_data.update({"response_action":"print_leaderboard"})
        #send this new information to all clients, they will just print this on their screens
        self.PassOn(new_data);
    
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
    
    def Networ(self, data):
        print "event listed at server side"
        action = data['request_action']
        if action == LANDED_SUCCESSFULLY:
            self.AddToSelfScore(data)
    
        

class LunarLanderServer(Server):
    channelClass = ServerChannel
    
    def __init__(self, *args, **kwargs):
        self.id = 0
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
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
        player.Send({"action": "initial", "lines": dict([(p.id, {"color": p.color, "lines": p.lines}) for p in self.players])})
        self.SendPlayers()
    
    def DelPlayer(self, player):
        print "Deleting Player" + str(player.addr)
        del self.players[player]
        self.SendPlayers()
    
    def SendPlayers(self):
        # TODO: Transmit data to players/clients
        self.SendToAll({"action": "players", "players": dict([(p.id, p.color) for p in self.players])})
    
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
    

# get command line argument of server, port
if len(sys.argv) != 2:
    print "Lunar Lander Usage:", sys.argv[0], "host:port"
    print "e.g.", sys.argv[0], "localhost:31425"
else:
    host, port = sys.argv[1].split(":")
    s = LunarLanderServer(localaddr=(host, int(port)))
    s.Launch()