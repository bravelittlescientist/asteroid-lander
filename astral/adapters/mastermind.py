from astral.adapters.Net import TCPServer,errors
from base_adapter import ClientAdapter
import socket
import threading
import time

class server_adapter(TCPServer):
    def __init__(self,gameserver,host="127.0.0.1",port=1919):
        TCPServer.__init__(self)
        self.gameserver = gameserver
        self.host = host
        self.port = port
        self.messages = []
        self.addr = None
        self.Send = lambda data:0
    def sendback(self,data):
        self.send_data(data)
    def send_to_socket(self,sock,data):
        self.sending_socket = sock
        self.send_data(data)
    def remove_socket(self,sock):
        """Add a try except here"""
        try:
            TCPServer.remove_socket(self,sock)
        except ValueError:
            import traceback
            traceback.print_exc()
    def input_func(self,sock,host,port,address):
        """This occurs for each socket we hear from right before handle_data is called"""
        self.addr = address
        self.Send = lambda data:self.send_to_socket(sock,data)
    def handle_data(self,data,addr=None,send=None):
        """This occors on incoming data, right after input_func is called, but only if data is clean"""
        if not addr:
            addr = self.addr
        if not send:
            send = self.Send
        self.messages.append((self.addr,self.Send,data))
    def client_disconnect_func(self,sock,host,port,address):
        """Client disconnected"""
        self.messages.append((address,lambda data:0,{"action":"disconnected"}))
    def update(self):
        #The threads should already be listening
        for a in self.messages[:]:
            self.gameserver.handle_data(*a)
            self.messages.remove(a)
    def _start(self):
        self.ending = False
        try:
            self.connect(self.host,self.port)
        except:
            print("can't host")
            self.handle_data({"action":"error","value":"hosting_error"})
            self.ending = True
            return
        self.serve_forever()
        self.quit()
        self.ending = True
    def start(self):
        t = threading.Thread(target=self._start)
        t.daemon = True
        t.start()
        self.t =t 
    def close(self):
        try:
            self.quit()
        except:
            pass
        self.looping = False
        if self.sending_socket:
            self.sending_socket.close()
        if self.unconnected_socket:
            self.unconnected_socket.close()
        if getattr(self,"connected_sockets",None):
            for sock in self.connected_sockets:
                sock.close()
        #self.socketaddresses = {}
        while not self.ending:
            pass

from astral.adapters.Net import TCPClient,errors

class client_adapter(TCPClient,ClientAdapter):
    def __init__(self,gameclient,host="127.0.0.1",port=1919):
        TCPClient.__init__(self)
        ClientAdapter.__init__(self,gameclient,host,port)
        self.connect_to_server()
        try:
            self.connect(host,port)
        except:
            self.handle_disconnect()
            return
        self.handle_connect()
    def send_to_server(self,data):
        try:
            self.send_data(data)
        except:
            return
    def listen(self):
        if not self.connect_state:
            return
        try:
            data = self.check_for_data()
        except errors.SocketError:
            self.handle_disconnect()
            return
        if data:
            self.handle_data(data)
        self.flush()
    def close(self):
        self.quit()
        
adapter_hook = {("server","tcp"):server_adapter,("client","tcp"):client_adapter}