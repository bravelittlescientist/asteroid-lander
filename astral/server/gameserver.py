import time
from astral.scene import Registry
from astral.server.elements import Player,Actor
from astral.log import PrintMessageLog as MessageLog
import random
import astral.adapters

def log(*msg):
    msg = " ".join([str(x) for x in msg])
    l.debug(msg)

class GameServer(object):
    def __init__(self):
        self.running = True
        self.update_rate = .033
        self.max_players = 100
        
        self.update_count = 0 #Track the number of world updates we have run
        self.objects = Registry()
        self.players = Registry()
        self.transport = None
        self.last_update = None
        self.next_update = self.update_rate
        
        self.state_history = []
        self.max_state_history = 10
        
        self.current_player = None
        self.message_log = MessageLog(mirror=self.mirror_message)
        global l
        l = self.message_log
        self.init()
    def disconnect(self):
        """How to initiate a disconnection from the server"""
        if self.transport:
            self.transport.close()
            self.transport = None
    def handle_data(self,address,send_func,data):
        """Unpack message data and call appropriate method."""
        if type(data)!=type({}):
            return
        p = self.get_player(address,send_func)
        if p.error:
            p.send({"action":"error","value":p.error})
            return
        msg_type = data.get("action","")
        del data["action"]
        f = getattr(self,"msg_"+msg_type,None)
        if not f:
            log("Unhandled message type",msg_type)
            return
        f(**data)
    def host(self,host,port,library="podsixnet",protocol="tcp"):
        """Begin hosting"""
        self.host = host
        self.port = port
        self.library = library
        self.protocol = protocol
        adapter = astral.adapters.get_adapter(library,"server",protocol)
        self.transport = adapter(self,host,port)
        self.transport.start()
    def sendback(self,msg):
        """Send a message back to the currently talking player"""
        if self.current_player:
            self.current_player.send(msg)
    def mirror_message(self,m):
        """Pack up a message from the log and send it to it's destination"""
        #Send to everyone
        if m["destination"] == "world":
            players = self.players.values()
        else:
            players = [p for p in [self.players.get(m["destination"],None)] if p]
        log("send",m,"to",players)
        for p in players:
            p.send({"action":"message","data":m})
    def init(self):
        """Game specific init function"""
    def get_player(self,addr,send):
        """Get player for address. If player doesn't exist, create one."""
        if addr in self.players:
            self.current_player = p = self.players[addr]
            return p
        self.current_player = p = Player(addr,send)
        if len(self.players)>=self.max_players:
            p.error = "server_full"
            return p
        self.players[addr] = p
        p.send({"action":"handshake","key":addr,"server_state_rate":p.state_rate})
        log(addr,"logged in. current players",self.players)
        return p
    def msg_authenticate(self,data):
        """Check player authentication. Kick from server with
        error message if authentication doesn't match. In the default
        case, authenticates everyone."""
        log("Trying to authenticate with",data)
        self.current_player.init()
        self.player_joined(self.current_player)
        self.authenticate(self.current_player)
    def player_joined(self,player):
        """Override to do something when a player joins"""
    def authenticate(self,player):
        """Tells the player they are authenticated. May also do some 
        other housecleaning (loading player values from storage etc)"""
        player.authenticated = True
        player.send({"action":"authenticated","value":"You've been authenticated"})
    def ping_player(self,player):
        player.send({"action":"ping"})
        player.ping_start = time.time()
    def msg_pong(self):
        player = self.current_player
        diff = time.time() - player.ping_start
        player.ping_count += 1
        player.total_ping += diff
        player.latency = player.total_ping/float(player.ping_count)
        log("player",player.addr,"ping",diff,"avg",player.latency)
    def remove_player(self,k):
        log("delete player",k)
        if k in self.players:
            self.players[k].remove(self)
            del self.players[k]
        log("players",self.players)
    def timeout_players(self):
        for k in self.players.keys():
            player = self.players[k]
            if time.time()-player.ping_start > 5:
                self.ping_player(player)
            #~ if time.time()-self.players[k].lastack>2:
                #~ self.remove_player(k)
    def msg_disconnected(self):
        self.remove_player(self.current_player.addr)
    def logoff(self,key):
        self.remove_player(key)
    def update(self):
        if self.transport:
            self.transport.update()

        if not self.last_update:
            self.last_update = time.time()
        dt = (time.time()-self.last_update)
        self.last_update = time.time()
        self.timeout_players()
        
        self.next_update -= dt
        if self.next_update <= 0:
            self.update_count += 1
            self.next_update = self.update_rate
            self.update_objects()
            self.update_sim()
        
        states = self.objects.get_state()
        self.state_history.append((self.update_count,states))
        while len(self.state_history)>self.max_state_history:
            del self.state_history[0]
        for p in self.players.values():
            if time.time()-p.laststate_time>p.state_rate:
                p.laststate_time = time.time()
                p.send_world(self.filter_states(states,p),self.update_count)
    def filter_states(self,states,player):
        """Return a set of object states valid for a specific player's interest. By default, 
        all objects are interesting to all players. Override to change behavior"""
        return states
    def update_objects(self):
        for k in self.objects.keys():
            o = self.objects[k]
            o.update(self)
            if o.kill:
                del self.objects[k]
    def update_sim(self):
        """Update the simulation. Subclass for more stuff"""
    def msg_input(self,data,update_count):
        """Receive input data for a specific update, generally meant to be character control
        information from a client"""
        for okey in self.current_player.actors:
            o = self.objects[okey]
            o.inputs[update_count] = data