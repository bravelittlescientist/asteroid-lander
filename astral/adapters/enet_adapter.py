import enet

from base_adapter import ServerAdapter,ClientAdapter

import sys,os
sys.path.append(os.path.abspath(__file__).replace("\\","/").rsplit("/",1)[0])

def enet_dispatch(event,ob):
    if event.type==enet.EVENT_TYPE_NONE:
        return
    if event.type==enet.EVENT_TYPE_CONNECT:
        f = getattr(ob,"handle_connect",None)
    if event.type==enet.EVENT_TYPE_DISCONNECT:
        f = getattr(ob,"handle_disconnect",None)
    if event.type==enet.EVENT_TYPE_RECEIVE:
        f = getattr(ob,"handle_receive",None)
    if f:
        f(event)
def hostport(address):
    return address.host,address.port

class server_adapter(ServerAdapter):
    def __init__(self,gameserver,host="127.0.0.1",port=1919):
        super(server_adapter,self).__init__(gameserver,host,port)
        self.host = None
    def handle_receive(self,event):
        data = eval(event.packet.data)
        def cli_send(data):
            event.peer.send(0,enet.Packet(repr(data)))
        self.gameserver.handle_data(hostport(event.peer.address),cli_send,data)
    def start(self):
        self.host = enet.Host(enet.Address(self.host, self.port), 1000, 0, 0, 0)
    def update(self):
        event = self.host.service(0)
        enet_dispatch(event,self)
    def handle_connect(self,event):
        pass
    def handle_disconnect(self,event):
        self.gameserver.remove_player(hostport(event.peer.address))
    def close(self):
        self.host = None


class client_adapter(ClientAdapter):
    def __init__(self,gameclient,host="127.0.0.1",port=1919):
        super(client_adapter,self).__init__(gameclient,host,port)
        self.enet = enet.Host(None, 1, 0, 0, 0)
        self.server = self.enet.connect(enet.Address(self.host,self.port),1)
        self.connect_to_server()
    def send_to_server(self,data):
        self.server.send(0,enet.Packet(repr(data)))
    def listen(self):
        event = self.enet.service(0)
        enet_dispatch(event,self)
        self.flush()
    def close(self):
        self.server.disconnect()
    def handle_disconnect(self,event):
        super(client_adapter,self).handle_disconnect()
    def handle_connect(self,event):
        super(client_adapter,self).handle_connect()
    def handle_receive(self,event):
        data = eval(event.packet.data)
        self.handle_data(data)

adapter_hook = {("server","tcp"):server_adapter,("client","tcp"):client_adapter}