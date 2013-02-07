#Contains convenience items to help clients connect to servers

# How matchmaking works:
#
#   server always running
#
#   game client connects to matching server to get list of games
#   list of games is periodically updated
#   client disconnects from matchmaking and connects to game server
#
#   game server connects to matching server and registers with it
#   game server periodically updates its status to matching server
#

import sys
sys.path.append("..")
from astral.client import gameclient
from astral.server import gameserver
from astral.server import elements

class GameConnection(object):
    def __init__(self):
        self.host = ""
        self.port = 0
        self.players = 0
    def __repr__(self):
        return "Host: %s - Port: %s - # of players: %s"%(self.host,self.port,self.players)

class MatchServer(gameserver.GameServer):
    def msg_register(self,host,port,players):
        print "msg register"
        c = GameConnection()
        c.host = host
        c.port = port
        c.players = players
        self.current_player.game_connection = c
    def get_servers(self):
        return [p.game_connection for p in self.players.values()]
    
class ServerToServer(gameclient.GameClient):
    def register(self,server):
        print "register",server.host,server.port,len(server.players)
        self.send({"action":"register","host":server.host,"port":server.port,"players":len(server.players)})
    
class MatchClient(gameclient.GameClient):
    def connect_to_matchmaker(self,host,port):
        pass
    def list_servers(self):
        pass
        
class testGameServer(gameserver.GameServer):
    matchhost = "127.0.0.1"
    matchport = 1000
    def host(self,*args,**kwargs):
        super(testGameServer,self).host(*args,**kwargs)
        self.server_to_server = ServerToServer()
        self.server_to_server.connect(self.matchhost,self.matchport,"podsixnet")
        self.server_to_server.announce({})
        self.server_to_server.register(self)
    def update(self):
        super(testGameServer,self).update()
        self.server_to_server.listen()
    def player_joined(self,p):
        super(testGameServer,self).player_joined(p)
        self.server_to_server.register(self)
    def remove_player(self,k):
        super(testGameServer,self).remove_player(k)
        self.server_to_server.register(self)
    def disconnect(self):
        self.server_to_server.disconnect()
        
def test():
    match_server = MatchServer()
    match_server.host("127.0.0.1",1000,"podsixnet")
    
    gameserver1 = testGameServer()
    gameserver1.host("127.0.0.1",93)
    
    for i in range(5):
        gameserver1.update()
        match_server.update()
        print match_server.get_servers()
    assert len(match_server.players)==1
    
    gameserver2 = testGameServer()
    gameserver2.host("127.0.0.1",94)
    for i in range(5):
        gameserver2.update()
        match_server.update()
        print match_server.get_servers()
    assert len(match_server.players)==2
    
    gameserver1.disconnect()
    gameserver1.update()
    for i in range(5):
        gameserver2.update()
        match_server.update()
        print match_server.get_servers()
    assert len(match_server.players)==1
    
    p = elements.Player()
    gameserver2.players[0] = p
    gameserver2.player_joined(p)
    for i in range(5):
        gameserver2.update()
        match_server.update()
        print match_server.get_servers()
    assert match_server.get_servers()[0].players == 1
    
    p = elements.Player()
    gameserver2.players[1] = p
    gameserver2.player_joined(p)
    p = elements.Player()
    gameserver2.players[2] = p
    gameserver2.player_joined(p)
    gameserver2.remove_player(0)
    for i in range(5):
        gameserver2.update()
        match_server.update()
        print match_server.get_servers()
    assert match_server.get_servers()[0].players == 2
test()