import socket

from base_adapter import ServerAdapter,ClientAdapter
from astral.adapters.PodSixNet.Channel import Channel
from astral.adapters.PodSixNet.Server import Server

class ClientChannel(Channel):
    player = None
    def Network(self, data):
        self._server.gameserver.handle_data(self.addr,self.Send,data)
    def handle_close(self):
        self.Network({"action":"disconnected"})
        Channel.handle_close(self)

class server_adapter(ServerAdapter):
    def start(self):
        Server.channelClass = ClientChannel
        self.podsix = Server(None,(self.host,self.port))
        self.podsix.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 0)
        self.podsix.gameserver = self.gameserver
    def update(self):
        self.podsix.Pump()
    def close(self):
        self.podsix.close()
        
from astral.adapters.PodSixNet.Connection import ConnectionListener

class client_adapter(ConnectionListener,ClientAdapter):
    def __init__(self,gameclient,host="127.0.0.1",port=1919):
        ConnectionListener.__init__(self)
        ClientAdapter.__init__(self,gameclient,host,port)
        self.Connect((host,port))
        self.connect_to_server()
    def send_to_server(self,data):
        self.Send(data)
    def Network(self, data):
        if self.connect_state == "connecting":
            self.handle_connect()
        self.handle_data(data)
    def Network_error(self,error):
        self.handle_data({"action":"error","value":error})
    def Network_disconnected(self,data):
        self.handle_disconnect()
    def listen(self):
        self.Pump()
        self.flush()
    def Pump(self):
        ConnectionListener.Pump(self)
        self.connection.Pump()
    def close(self):
        self.connection.close()

adapter_hook = {("server","tcp"):server_adapter,("client","tcp"):client_adapter}