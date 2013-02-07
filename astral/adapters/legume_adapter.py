import socket

from base_adapter import ServerAdapter,ClientAdapter

import sys,os
sys.path.append(os.path.abspath(__file__).replace("\\","/").rsplit("/",1)[0])

import legume
import legume.exceptions



class GenericMessage(legume.messages.BaseMessage):
    MessageTypeID = legume.messages.BASE_MESSAGETYPEID_USER+1
    MessageValues = {
        "action":"string 16",
        "data":"varstring"
    }
    def fromd(self,d):
        self.action.value = d["action"]
        self.data.value = repr(d)
        return self
    def tod(self):
        return eval(self.data.value)
legume.messages.message_factory.add(GenericMessage)

class server_adapter(ServerAdapter):
    def __init__(self,gameserver,host="127.0.0.1",port=1919):
        super(server_adapter,self).__init__(gameserver,host,port)
        self.legume = legume.server.Server()
        self.legume.OnMessage += self.handle_message
        self.legume.OnConnectRequest += self.handle_connect_request
    def handle_message(self,sender,message):
        def cli_send(data):
            sender.send_reliable_message(GenericMessage().fromd(data))
        self.gameserver.handle_data(sender.address,cli_send,message.tod())
    def handle_connect_request(self,sender,message):
        print "connect",sender.address
    def start(self):
        self.legume.listen((self.host,self.port))
    def update(self):
        self.legume.update()
    def close(self):
        self.legume.disconnect_all()
        self.legume._socket.close()
        self.legume = None

class client_adapter(legume.client.Client,ClientAdapter):
    def __init__(self,gameclient,host="127.0.0.1",port=1919):
        legume.client.Client.__init__(self)
        ClientAdapter.__init__(self,gameclient,host,port)
        self.OnMessage += self.handle_message
        self.OnConnectRequestAccepted += self.connected
        self.OnError += self.handle_error
        self.connect((host,port))
    def send_to_server(self,data):
        self.send_reliable_message(GenericMessage().fromd(data))
    def connected(self,sender,message):
        ClientAdapter.handle_connect(self)
    def handle_message(self,sender,message):
        ClientAdapter.handle_data(self,message.tod())
    def handle_error(self,ob,error):
        self.handle_data({"action":"error","value":error})
    def listen(self):
        self.update()
        self.flush()

adapter_hook = {("server","tcp"):server_adapter,("client","tcp"):client_adapter}