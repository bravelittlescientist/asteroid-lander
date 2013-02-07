import time
from astral import interpolator

class NetworkedProperty(object):
    """Definition of an object property meant to be networked, and by what algorithm
    the property should be syncronized across the server and the client"""
    def __init__(self,name,predicted=False,interpolation=None):
        """name - The property name. When mapped to an object will be object.name, 
            i.e. NetworkedProperty("y") -> object.y
        predicted - If True, will not be overwritten by the property state from the server, will
            instead use a predicted client-side value
        interpolation - How the property should be interpolated from an old state to a future state:
            one: set the new value when the timer reaches the future state
            zero: set the new value to the future state right away
            linear: use a linear function to interpolate from the old state to the future state
            log: use a logarithmic function - if far from future state, interpolate quickly; if close, interpolate slowly
            inverse: use an inverse logarithmic function, the closer to the future state the faster we get there"""
        self.name = name                     #the name of the property
        self.predicted = predicted          #whether this property can be predicted by the client
        self.interpolation = interpolation  #string defining an interpolation method or None to pick based on datatype

class RemoteObject(object):
    """This object is managed on the server, but we keep a representation of the object locally."""
    def __init__(self,key=None,prediction_func=None):
        """key - unique key
        prediction_func - A function to run for client-side prediction:
            def prediction(object,input)
            Change object attributes according to given input"""
        self.key = key
        self.template = None
        self.is_owned = False  #Object is owned by current client
        self.buffered = []  #List of buffered states to interpolate
        self.last_state = {}   #Last state applied
        self.max_buffer = 5   #More buffers will be smoother but take a longer time to get to "now"
        self.buffer_skew = 1   #How fast to go through the buffers. Too fast is jerky, too slow and buffers fill up
        self.buffer_wait = 2   #How many states to buffer before interpolating, should be a lot less than max_buffer
        self.t = 0.0 #Progression between buffered state zero and buffered state one
        
        #Definition of networked properties
        self.properties = {}
        
        #Function to define how to apply input to our object state for one tick of simulation
        self.prediction_func = prediction_func
        self.use_prediction = False #Set this to true for any objects that should be using prediction

        self.prediction_buffer = {}  #Our predicted states at various times, for correction
        self.max_prediction_buffer = 30
        
        self.values = []
        
        self.init()
    def init(self):
        """Init function to override."""
    def add_property(self,property):
        """Add a new NetworkedProperty. Attributes are syncronized according to the server, but we can
        add these definitions to further configure how we deal with some of these properties."""
        self.properties[property.name] = property
    def apply_state(self,state):
        """Standard apply function to apply a state to a mob (mobile object). Sets attributes
        on self according to key/values in the state dictionary. Keys that start with '_' are
        metakeys and wont be applied.
        
        Example:
        ob = RemoteObject()
        ob.color = 'red'
        ob.size = 5
        ob.apply_state({'color':'green','_available_properties':['color','size']})
        ob.color -> 'green'
        ob.size -> 5
        ob._available_properties -> undefined"""
        for k in state:
            if k.startswith("_"):
                continue
            setattr(self,k,state[k])
    def buffer_state(self,state):
        """A new state has come in. Undiff it to previous state and add it to the buffer. 
        If it's the first state (no previous state to combine with), apply it."""
        if state.get("_force_apply",None):
            self.buffered[:] = []
        
        #Apply differences
        next_state = {}
        if self.buffered:
            next_state.update(self.buffered[-1])
        next_state.update(state)
        next_state["_time"] = time.time()-0.10
        self.buffered.append(next_state)
        
        while len(self.buffered)>self.max_buffer:
            del self.buffered[0]

        if len(self.buffered)==1:
            self.values = [x for x in state.keys() if not x.startswith("_")]
            self.apply_state(state)
    def get_state(self):
        """Similar to the server side get_state, but in this case we base our values
        on the first set of values the server told us about rather than hardcoding 
        the attributres we care about."""
        d = {}
        for k in self.values:
            d[k] = getattr(self,k)
        return d
    def apply_current_state(self):
        """Take current interpolated state out of the buffer
        apply that state to the object using our apply function.
        Only relevant if buffer_wait is greater than 1."""
        if len(self.buffered)<self.buffer_wait:
            return
        a = self.buffered[0]
        b = self.buffered[1]
        interp_method = {}
        for p in self.properties.values():
            if p.interpolation:
                interp_method[p.name] = p.interpolation
        state = interpolator.interpolate(a,b,self.t,interp_method)
        self.last_state = state
        if self.use_prediction and not state.get("_force_apply",None):
            self.last_state = {}
            for k in [x.name for x in self.properties.values() if x.predicted]:
                if k in state:
                    del state[k]
        self.apply_state(state)
    def increment_time(self,dt,server_rate):
        if len(self.buffered)<2 or len(self.buffered)<self.buffer_wait:
            return
        times = self.buffered[1]["_time"] - self.buffered[0]["_time"]
        rate_skew = float(times)/float(server_rate)   #Adjust to time events actually should have arrived
        if rate_skew < 1:
            rate_skew = 1
        self.t += dt/server_rate*self.buffer_skew*rate_skew
        next = 0
        if self.t>=1:
            self.t = 1
            next = self.t-1.0
        self.apply_current_state()
        if self.t>=1:
            del self.buffered[0]
            self.t = next
    def prediction(self,state,input,t):
        """Starting from state, at time t0,
        using input data, apply the state that would
        be correct at time t0+t
        Only called for objects with a prediction_func which are configued
        by the client as currently using prediction."""
        if not self.prediction_func or not self.use_prediction:
            return
        self.prediction_buffer[t] = {"state":self.get_state(),"input":input,"t":t}
        self.apply_state(state)
        self.prediction_func(self,input)
    def correct_prediction(self,t):
        """Compare predicted states with incoming states. If there
        are differences, rerun the prediction up till now"""
        if not self.use_prediction:
            return
        lowest = None
        highest = None
        for b in self.buffered:
            if not lowest or b["_update_count"]<lowest["_update_count"]:
                lowest = b
            if not highest or b["_update_count"]>highest["_update_count"]:
                highest = b
        bad = []
        if highest:
            b = highest
            uc = b["_update_count"]
            if uc in self.prediction_buffer:
                p = self.prediction_buffer[uc]
                bt = {}
                for k in [x for x in b if not x.startswith("_")]:
                    bt[k] = b[k]
                if interpolator.state_diff(bt,p["state"]):
                    input = p["input"][:]
                    if ".p" in input:
                        input.remove(".p")
                    bad.append({"state":bt,"input":p["input"],"t":uc})
        if bad:
            most_recent = bad[-1]
            state = most_recent["state"]
            for uc in range(most_recent["t"],t+1):
                if uc not in self.prediction_buffer:
                    continue
                input = self.prediction_buffer[uc]["input"]
                self.prediction(state,input,uc)
                state = self.get_state()
                del self.prediction_buffer[uc]
        if not lowest:
            return
        for c in self.prediction_buffer.keys():
            if c<lowest["_update_count"]:
                del self.prediction_buffer[c]
        while len(self.prediction_buffer.keys())>self.max_prediction_buffer:
            del self.prediction_buffer[min(self.prediction_buffer.keys())]

class Mob(RemoteObject):
    """A RemoteObject with a position
    properties: x,y
    x and y can be predicted, and are interpolated with 'linear'"""
    def init(self):
        self.add_property(NetworkedProperty("x",predicted=True,interpolation="linear"))
        self.add_property(NetworkedProperty("y",predicted=True,interpolation="linear"))