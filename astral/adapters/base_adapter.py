import sys,os
d = os.path.abspath(__file__).replace("\\","/").rsplit("/",1)[0]
sys.path.append(d+"/../..")

class AdapterNotImplemented(Exception):
    pass
    
class ServerAdapter(object):
    def __init__(self,gameserver,host="127.0.0.1",port=1919):
        self.gameserver = gameserver
        self.host = host
        self.port = port
    def start(self):
        pass
    def update(self):
        pass

class ClientAdapter(object):
    def __init__(self,gameclient,host="127.0.0.1",port=1919):
        self.gameclient = gameclient
        self.host = host
        self.port = port
        self.connect_state = None
        self.send_buffer = []
    def send(self,data):
        if not self.connect_state=="connected":
            self.send_buffer.append(data)
            return
        self.send_to_server(data)
    def flush(self):
        if self.connect_state=="connected" and self.send_buffer:
            for d in self.send_buffer:
                self.send(d)
            self.send_buffer = []
    def connect_to_server(self):
        self.connect_state = "connecting"
    def handle_connect(self):
        self.handle_data({"action":"connected"})
        self.connect_state = "connected"
    def handle_disconnect(self):
        if self.connect_state == "connecting":
            self.handle_data({"action":"error","value":"connection_error"})
        self.handle_data({"action":"disconnected"})
        self.connect_state = None
    def handle_data(self,data):
        self.gameclient.handle_data(data)
    def close(self):
        pass

#Some magic, import all possible adapters so they can be selected from code
def get_adapter(text,mode,protocol="tcp"):
    adapter = None
    try:
        m = __import__("astral.adapters."+text,locals(),globals(),fromlist=["adapter"],)
        adapter = m.adapter_hook.get((mode,protocol),None)
    except ImportError:
        import traceback
        traceback.print_exc()
    if not adapter:
        raise AdapterNotImplemented("No adapter implemented for %s as a %s %s"%(text,protocol,mode))
    return adapter

