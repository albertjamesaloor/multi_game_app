import socket
import pickle


class Network:
    def __init__(self, found_server):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server =  found_server
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p
    

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
    
    def close(self):
        self.client.close()
