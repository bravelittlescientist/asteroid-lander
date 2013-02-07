"""The scene module"""

import random

def gen_key():
    """Generates a random 8 character key to uniquely identify an object"""
    chars = []
    for i in range(8):
        chars.append(random.choice("0123456789BCDFGHJKLMNPQRSTVWXZ"))
    return "".join(chars)

class Registry(dict):
    """Registry is a dictionary containing references to objects contained in a scene."""
    def gen_key(self):
        """Continues to generate keys until it finds one we haven't used yet."""
        while 1:
            key = gen_key()
            if key not in self:
                return key
    def add(self, object, key=None):
        """Adds an object to the registry. Can manually assign the object a key by argument, use
        a key already assigned to object.key, or leave both of these values empty or none to
        have the registry generate a random key to assign the object. Returns the object
        with object.key set."""
        if key is None:
            key = getattr(object,"key",None)
        if key is None:
            key = self.gen_key()
        self[key] = object
        object.key = key
        return object
    def delete(self,key):
        """Deletes object belonging to key, if it exists."""
        if key in self:
            ob = self[key]
            del self[key]
            return ob
        return None
    def all(self):
        """Returns a list of all the objects for easy iteration."""
        return self.values()
    def get_state(self):
        """Calls object.get_state() for each object in the Registry and returns
        a dictionary mapping object keys to those states. This dictionary can
        be easily sent over the network in order to recreate the registry remotely."""
        d = {}
        for k in self.keys():
            o = self[k]
            if hasattr(o,"get_state"):
                d[k] = o.get_state()
        return d