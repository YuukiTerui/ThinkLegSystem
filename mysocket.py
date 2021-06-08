# coding: utf-8

import socket
import threading

class MySocket():
    MSGLEN = 1024
    DATASIZE = 2**10
    def __init__(self, host, port, kind) -> None:
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CLIENT_NUM = 10
        self.is_running = False
        self.is_connected = False
        if kind == 'server':
            self.init_server(host, port)
        else:
            self.init_client(host, port)

    def init_server(self, host, port):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.bind((host, port))
        self.socket.listen(self.CLIENT_NUM)
        print(f'Server: {self.socket}')
        print('Waiting for connections...')

    def run_server(self):
        while self.is_running:
            client, address = self.socket.accept()
            #client.settimeout(60)
            t = threading.Thread(target=self.connect_client, args=(client, address))
            t.setDaemon(True)
            t.start()
        print('stop server')
    
    def connect_client(self, client, address):
        while self.is_connected:
            data = client.recv(MySocket.DATASIZE).decode('utf-8')


    def init_client(self, host, port):
        self.socket.connect((host, port))

    def send(self, msg):
        totalsend = 0
        while totalsend < MySocket.MSGLEN:
            sent = self.socket.send(msg[totalsend:])
            if sent == 0:
                raise RuntimeError('socket connection broken')
            totalsend += sent
        
    def receive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MySocket.MSGLEN:
            chunk = self.socket.recv(min(MySocket.MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError('socket connection broken')
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)
        

def main():
    host = 'localhost'
    port = 12345

    server = MySocket(host, port, 'server')



if __name__ == '__main__':
    main()
