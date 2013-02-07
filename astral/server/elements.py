#Contains objects which live on the server and mirror to all clients
import time
from astral import interpolator

class Player(object):
    """A connected client. May own Actors"""
    def __init__(self,addr=None,send=None):
        self.addr = addr
        if send:
            self.send = send
        self.init()
    def init(self):
        """Resets the player, important for reconnections"""
        self.actors = set()   #Ids of the objects that we own (don't store the objects, otherwise hard to delete)
        self.lastack = time.time()
        self.ping_start = 0                 #Last time a ping was requested
        self.latency = 0                    #Measured ping time for this client, used for prioritization techniques
        self.ping_count = 0               #Number of times pinged
        self.total_ping = 0                 #Total amount of ping delay measured
        self.error = None                  #Some error with the player, cheating, or not supposed to be here
        self.authenticated = False      #Whether player has completed log in or not
        self.laststate = {}               #Contains the last sent object states
        self.state_rate = 0.05
        self.laststate_time = time.time()-self.state_rate
    def get_object(self,server):
        """Helper for traditional game model where each player only controls one character"""
        return server.objects[list(self.actors)[0]]
    def get_objects(self,server):
        """Return currently owned objects"""
        return [server.objects[key] for key in self.actors if key in server.objects]
    def send(self,msg):
        """Send a message to the player, real send function set by server from the connected socket"""
    def owns_object(self,object):
        """Server informs us that we own an actor"""
        self.actors.add(object.key)
        self.send({"action":"player_owns","keys":list(self.actors)})
    def disowns_object(self,object):
        """Server takes ownership of an actor"""
        self.actors.remove(object.key)
        self.send({"action":"player_owns","keys":list(self.actors)})
    def remove(self,server):
        """We must tell all of our owned objects that we are disconnecting, so they can either transfer
        ownership or be deleted themselves."""
        for owned in self.actors:
            server.objects[owned].owner_disconnected(server,self)
    def send_world(self,states,update_count):
        """Do a difference between the sending state and the last sent state
        Send along this change, making sure not to include keys of objects
        that are no longer with us. Up to the client to delete the objects
        that are not found in the world state"""
        cs = {}
        for s in states:
            cs[s] = interpolator.state_diff(self.laststate.get(s,{}),states[s])
        for s in cs.keys():
            if s not in states:
                del cs[s]
        self.send({"action":"worldupdate","states":cs,"update_count":update_count})
        self.laststate = states.copy()
        
class Actor(object):
    """Some object the server knows about which has some replication on the client side"""
    def __init__(self):
        self.key = None
        self.template = None   #Helps in how to create the object on the local end
        self.kill = 0
        self._force_apply = 0
        self.values = ["template","_force_apply"]
        self.init()
    def init(self):
        """Overwrite for customized init statements"""
    def get_state(self):
        """Overwrite this method to generate a passable dictionary
        of the important networked state. Default case maps every
        attribute listed in self.values"""
        d = {}
        for k in self.values:
            d[k] = getattr(self,k)
        return d
    def update(self,server):
        """Overwrite to control the gamelogic of the object on the server side"""
    def owner_disconnected(self,server,owner):
        """What happens if we are owned by someone, and our owner is deleted"""
    def warp(self):
        """Every time we are warped, the client needs to know not to interpolate position.
        Easiest way to do this is to just increment a warp counter. Every time it is changed,
        the key will show up on the client, and it will know to reset the state."""
        self._force_apply += 1
        
class Mob(Actor):
    """A movable object on a 2d plane."""
    def init(self):
        self.x = 0
        self.y = 0
        self.template = "Mob"
        self.values += ["x","y"]
        self.inputs = {}   #Input data for each tick
    def update(self,server):
        """Process incoming inputs"""
        times = self.inputs.keys()
        times.sort()
        for time in times:
            if time<server.update_count:
                data = self.inputs[time]
                del self.inputs[time]
                self.process_input(time,data)
    def process_input(self,time,data):
        """
        Overwrite to define game logic.
        
        Actually carry out a specific timestep of action. Data contains the state of the object's
        inputs at that timestep, but not the state at that timestep. It is assumed that the object
        state when this is run will match the state of the given timestep, as ALL input times are played
        back IN ORDER.
        """
    def owner_disconnected(self,server,owner):
        self.kill = 1
