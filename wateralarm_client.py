#!bin\python
import datetime
import socket as s
import threading
import time

class mySocket_client(s.socket):
    """Special designed class for Water-Stations-Alarm project"""
    def __init__(self, ip, port, ka_msg, set_timeout=None):
        s.socket.__init__(self)
        if set_timeout is not None: self.set_timeout(set_timeout)
        self._ka_time = 15
        self.ip = ip
        self.port = port
        self.ka_msg = ka_msg

    def run_client(self):
        with self:
            print('connecting to host, at ip:{},port{}'.format(
                                            self.ip, self.port))
            self.connect((self.ip, self.port))
            print('connected!')
            self.client_handler(self.ka_msg)

    def client_send(self, msg):
        __name = '[client_send]'
        totalsent = 0
        while totalsent < len(msg):
            sent = self.send(msg[totalsent:].encode())
            if sent == 0:
                raise RuntimeError(__name, "socket connection broken")
            totalsent = totalsent + sent

    def client_receive(self, msg):
        __name = '[client_receive]'
        chunks = []
        bytes_recd = 0
        while bytes_recd < len(msg):
            chunk = self.recv(min(len(msg) - bytes_recd, 2048)).decode()
            if chunk == '':
                raise RuntimeError(__name, "socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)

    def client_handler(self,client_recv_msg):
        __name = '[client handler]'
        while True:
            try:  # checks if client exists
                print(__name,'receiving message...')
                msg_rcvd = self.client_receive(client_recv_msg)
                print(__name,'message received:{}'.format(msg_rcvd))
            except self.timeout:
                print(__name,'connection timed out!')
            except Exception as e:
                print(__name,e)

            if msg_rcvd == self.ka_msg:
                try:
                    with open('./client_status.txt','r') as f:
                        self.client_send(''.join(f.readlines()))
                except Exception as e:
                    print(__name, e)