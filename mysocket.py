# coding: utf-8

import socket

class MySocket():
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.socket.connect((host, port))

    def send(self, msg):
        totalsend = 0
        while totalsend < MSGLEN:
            sent = self.socket.send(msg[totalsend:])
            if sent == 0:
                raise RuntimeError('socket connection broken')
            totalsend += sent
        
    def receive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.socket.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError('socket connection broken')
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)
        