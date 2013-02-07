import pygame
import time

from astral.scene import Registry
from astral.client import local
from astral.log import MessageLog
import astral.adapters

def log(*msg):
    return
    print(" ".join([str(x) for x in msg]))

class GameClient(object):
    """A single client by which a player will interact with the game. Contains a representation
    of the world according to the server, and all of the objects in that world. Knows
    how to connect and disconnect from a server. Buffers input commands by the player
    to send to the server. Interpolates between world states to make object transitions appear
    smooth when updating those states at a much lower rate."""
    remote_classes = local.__dict__
    def __init__(self):
        """Initializes the gameclient, starting with a blank Registry"""
        self.objects = Registry()
        self.client_key = None
        self.owned = []
        self.predict_owned = True
        self.transport = None
        self.lastack = time.time()
        self.running = True
        
        self.update_rate = .033
        self.last_update = None
        self.interpolation_rate = .02
        self.last_interpolation = None
        self.next_update = self.update_rate
        self.updates = {}
        self.keep_updates = 10
        
        self.update_count = None  #Starts in sync with server and then gets ahead
        self.server_update_count = None #Last update count we received from the server
        self.rate_skew = 2   #How fast to increment the update counter
        self.max_count_skew = 10  #How far different the update rate and server update rate before we adjust skew
        
        self.input_buffer = {}   #List of inputs to send out
        self.input_rate = .033  #Should match server update rate
        self.next_input = self.input_rate
        
        self.message_log = MessageLog()
        
        self.init()
    def init(self):
        """Runs after the GameClient is created. Override."""
        pass
    def connect(self,host,port,library="podsixnet",protocol="tcp"):
        """Connects to a server, should be a subclass of astral.server.gameserver.GameServer.
        host - host of the server
        port - port of the server
        library - which socket library adapter to use. Should be the same as the server we are connecting to.
        protocol - 'tcp' or 'udp', some socket libraries allow you to choose; most are fixed and this is ignored"""
        adapter = astral.adapters.get_adapter(library,"client",protocol)
        self.transport = adapter(self,host,port)
    def handle_data(self,data):
        """data is a dictionary corresponding to a message we received from the server.
        Will look up the method msg_{data["action"]} and pass the data into that method as kwargs.
        
        Example:
        data = {"action":"lose_health","amount":5}
        
        will call self.msg_lose_health(amount=5)"""
        log(data)
        if type(data)!=type({}):
            return
        msg_type = data.get("action","")
        del data["action"]
        f = getattr(self,"msg_"+msg_type,None)
        if not f:
            log("Unhandled message type",msg_type)
            return
        f(**data)
    def disconnect(self):
        """How to initiate a disconnection from the server. Puts client in a state where it could reconnect."""
        if self.transport:
            self.send({"action":"disconnected"})
            self.transport.close()
            self.transport = None
    def msg_error(self,value):
        """Server reported an error of some kind. Should override this method to handle different kinds of errors."""
        log(value)
    def msg_connected(self):
        """Server accepted our connect request. Should override this method."""
    def msg_disconnected(self):
        """Server has forcibly disconnected us. We may have requested a logout procedure or not.
        Put the game in some state to allow player to reconnect, or at least let them know what
        happened. Should override this method."""
        self.disconnect()
    def listen(self):
        """Listens for incomming messages, sends buffered input, and does interpolation and prediction.
        Call every frame."""
        if self.transport:
            self.transport.listen()
            
        if not self.last_update:
            self.last_update = time.time()
        dt = (time.time()-self.last_update)
        self.last_update = time.time()
        
        if not self.update_count:
            return

        self.tick()
        
        if not self.last_interpolation:
            self.last_interpolation = time.time()
        if time.time()-self.last_interpolation>self.interpolation_rate:
            self.interpolate_objects()
            self.last_interpolation = time.time()
        
        self.next_update -= dt*self.rate_skew
        if self.next_update <= 0:
            self.next_update = self.update_rate
            self.update_count += 1
            self.input_buffer[self.update_count] = []
            #print self.update_count-self.server_update_count
            self.update_objects()
        if self.update_count-self.server_update_count>self.max_count_skew:
            self.rate_skew = 0.75
        elif self.server_update_count-self.update_count<self.max_count_skew:
            self.rate_skew *= 1.25
            
        self.next_input -= dt
        if self.next_input <= 0:
            self.next_input = self.input_rate
            self.send_input()
    def buffer_action(self,action):
        """Add an action (player input) to the current tick actions, to be sent to server in
        set increments. If client state is too far ahead of server, actions will be ignored."""
        #Dont buffer inputs for states we dont have (we are too far ahead of server state)
        if self.update_count not in self.input_buffer:
            return
        current_input = self.input_buffer[self.update_count]
        if action not in current_input:
            current_input.append(action)
        self.input_buffer[self.update_count] = current_input
    def send_input(self):
        """Does the actual sending of buffered input."""
        keys = self.input_buffer.keys()
        keys.sort()
        for k in keys:
            if ".p" in self.input_buffer[k]:
                self.send({"action":"input","data":self.input_buffer[k],"update_count":k})
                del self.input_buffer[k]
    def msg_ping(self):
        """Server is pinging us, pong back"""
        self.send({"action":"pong"})
    def send(self,data):
        """Sends data across server"""
        if self.transport:
            self.transport.send(data)
    def announce(self,data={}):
        """Call when we are connected with the server (communication is open)
        but have not yet given the server information about this client. Data could be
        username and password or other stuff"""
        self.send({"action":"authenticate","data":data})
    def logoff(self):
        """Tell server we are logging off, doesn't actually disconnect."""
        self.send({"action":"logoff","value":self.client_key})
    def msg_handshake(self,key,server_state_rate):
        """Server is telling us some details about our connection after connection and authentication.
        key - the key assigned to our specific client
        server_state_rate - how often in seconds the server intends to send us an updated world state"""
        self.client_key = key
        self.server_state_rate = server_state_rate
        log("assign key",self.client_key,"to",self)
    def msg_player_owns(self,keys):
        """Server is informing us of objects which this client owns and can send input for."""
        self.owned = keys
    def msg_authenticated(self,value):
        """Server has accepted our announce()"""
        log(value)
    def msg_worldupdate(self,states,update_count):
        """The server sent us an updated world state.
        states - A dictionary mapping object keys to object states. States may be partial and 
            need to be combined with the last known state. We will need to interpolate between
            known states to get a smooth display.
        update_count - each time the server updates its simulation it increases the value of its
            current update. update_count is the identifier of which update states belongs to. If
            we get an update older than the last update we applied, we may need to go back
            in time and fix our state of the world according to what happened in the past."""
        self.server_update_count = update_count
        if not self.update_count:
            self.update_count = update_count
            self.input_buffer[self.update_count] = []
        self.updates[update_count] = states
        if len(self.updates)>self.keep_updates:
            keys = self.updates.keys()
            keys.sort()
            del self.updates[keys[0]]
        
        for key in states:
            state = states[key]
            state["_update_count"] = update_count
            if key not in self.objects:
                o = self.objects[key] = self.create_local(key,state)
            o = self.objects[key]
            o.buffer_state(state)
        for key in self.objects.keys():
            if key not in states:
                del self.objects[key]
    def create_local(self,key,state):
        """Create a local instance of a remote object.
        Use the values in the state as a guide for how it should be created.
        Assign its key.
        By default, will pick a class from client.local matching the template"""
        cls = self.remote_classes[state.get("template","RemoteObject")]
        o = cls(key)
        o.use_prediction = key in self.owned and self.predict_owned
        o.is_owned = key in self.owned
        return o
    def update_objects(self):
        """Run prediction or other updates on local copies of objects."""
        for k in self.objects:
            if not k in self.owned:
                continue
            o = self.objects[k]
            if self.update_count-1 in self.input_buffer:
                d = self.input_buffer[self.update_count-1]
                #Only predict states we haven't predicted yet
                if ".p" in d:
                    continue
                o.prediction(o.last_state,d,self.update_count-1)
                o.correct_prediction(self.update_count-1)
                d.append(".p")
    def interpolate_objects(self):
        """Increase every objects .t value and apply states"""
        for o in self.objects.all():
            o.increment_time(self.interpolation_rate,self.server_state_rate)
    def tick(self):
        """Something that happens every frame. Override."""
    def input(self):
        """Overwrite for actual input."""
    def msg_message(self,data):
        """Incoming message for the log, adds it to self.message_log."""
        self.message_log.log(**data)