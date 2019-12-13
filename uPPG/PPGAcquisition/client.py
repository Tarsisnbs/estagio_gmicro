import socket

class MySocket:

    def __init__(self,host="192.168.0.108",port=3000):

        self.sock = socket.socket()
        self.sock.connect((host, port))


    def get_data(self):
        return self.sock.recv(1024)
    
    def send_data(self, data):
        self.sock.send(str.encode(data))

