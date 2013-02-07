"""Megalithic logging module
Used for chat but also for system debug logging
Each message has an origin, a destination, and a set of types
Can search for specifics

Example:

>>>print logs.search(types=["chat","world"])
{"from":"system","to":"any","types":["chat","world","debug"],"message":"Server is going down soon"}
{"from":"joe","to":"any","types":["chat","world"],"message":"Aw, I was just starting to have fun"}
{"from":"sam","to":"joe","types":["chat","world"],"message":"If you whine, people will know your a whiner"}
"""

import time

class MessageLog(object):
    """Container to store logged messages. Messages may be chat messages from player to player,
    from player to server, from server to player, from player to all other players, etc."""
    def __init__(self,max_messages=None,mirror=None):
        """max_messages - the number of messages to store, when full the oldest message will be dropped
        mirror - a function to run on each message as it is added. Used to, for instance, broadcast chat 
            messages from the player when he adds a chat message to his log."""
        self.messages = []
        self.max_messages = max_messages
        self.mirror = mirror
    def log(self,source="",destination="",types=[],message=[],orig_time=None,**kwargs):
        """Logs a new message.
        source - who is sending the message
        destination - who should see it
        types - a list of 'tags' to help filter messages later
        message - a list of lines
        orig_time - the time the message was logged"""
        m = {"source":source,"destination":destination,
            "types":types,"message":message,"orig_time":orig_time,
            "recv_time":time.time()}
        self.messages.append(m)
        if self.max_messages and len(self.messages)>self.max_messages:
            del self.messages[0]
        if self.mirror and destination!="debug":
            self.mirror(m)
        return m
    def get_messages(self,source=None,destination=None,types=None):
        """Generator of existing messages, filter on source, destination, or types.
        
        source - only yield messages sent by 'source'
        destination - only yield messages sent to 'destination'
        types - only yield messages of these [types]"""
        for m in self.messages:
            y = True
            if source and m["source"] != source:
                y = False
            if destination and m["destination"] != destination:
                y = False
            if types:
                tt = False
                for t in types:
                    if t in types:
                        tt = True
                if not tt:
                    y = False
            if y:
                yield m
    def user_chat(self,ukey,message,channel="world"):
        """A convenient way to log chat messages.
        ukey - the key assigned to a given user sending the message
        message - the text user is sending
        channel - the chat channel the user is talking to"""
        self.log(source=ukey,destination=channel,message=message,types=["chat"])
    def user_private(self,ukey,message,tkey):
        """A convenient way to log private user to user messages, aka whisper or tell
        ukey - the key of the user sending a whisper
        message - the text message
        tkey - the key of the user to receive the whisper"""
        self.log(source=ukey,destination=tkey,message=message,types=["chat","private"])
    def system_message(self,msg,ukey):
        """A convenient way to log a message from the system to a user
        msg - the text to send
        ukey - the user to send a message to"""
        self.log(source="system",destination=ukey,message=msg,types=["info"])
    def system_announce(self,msg,channel="world"):
        """A convenient way to announce a server message to all users
        msg - text to send
        channel - chat channel to announce to"""
        self.log(source="system",destination=channel,message=msg,types=["info"])
    def debug(self,msg):
        """A convenient way to log a debug message. Depending on specific game
        config settings, you can show these or not.
        msg - text to send"""
        self.log(source="system",destination="debug",message=msg,types=["debug"])
    def format(self,m):
        """Format a message and return the string, overwrite to include more info
        Default formatting is just a string representation of the message dictionary"""
        return str(m)

class PrintMessageLog(MessageLog):
    """A customized messagelog which does a python print of messages
    as they come in"""
    def __init__(self,*args,**kwargs):
        kwargs["max_messages"] = 1
        super(PrintMessageLog,self).__init__(*args,**kwargs)
    def log(self,*args,**kwargs):
        """Logs the message like in MessageLog, but also prints the message to console"""
        super(PrintMessageLog,self).log(*args,**kwargs)
        print(self.format(self.messages[-1]))
    def format(self,m):
        """Don't print the whole message representation, just the text"""
        return m["message"]