#!bin\python
import socket as s


class MySocketClient(s.socket):
    """Special designed class for Water-Stations-Alarm project, client-side."""

    def __init__(self, ip, port, ka_msg, set_timeout=None):
        s.socket.__init__(self)
        if set_timeout is not None:
            self.set_timeout(set_timeout)
        self.ip = ip
        self.port = port
        self.ka_msg = ka_msg

    def run_client(self):
        """Connecting to server and starts client-handler."""
        __name = '[run_client]'
        with self:
            print(__name, 'connecting to host, at ip: {}, port: {}'.format(
                self.ip, self.port))
            self.connect((self.ip, self.port))
            print(__name, 'connected!')
            self.client_handler(self.ka_msg)

    def client_send(self, msg):
        """Sending 'msg' message to server."""
        __name = '[client_send]'
        total_sent = 0
        while total_sent < len(msg):
            sent = self.send(msg[total_sent:].encode())
            if sent == 0:
                raise RuntimeError(__name, "socket connection broken")
            total_sent = total_sent + sent

    def client_receive(self, msg):
        """Receives message from server and returns it."""
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

    def client_handler(self, client_recv_msg):
        """Receives message from server. If its Keep-Alive message ('ka_msg'),
        read data from 'client_status.txt' and send content to server."""
        __name = '[client handler]'
        while True:
            try:
                msg_rcvd = self.client_receive(client_recv_msg)
                print(__name, 'message received:{}'.format(msg_rcvd))
            except self.timeout:
                print(__name, 'connection timed out!')
            except Exception as e:
                print(__name, e)

            if msg_rcvd == self.ka_msg:
                try:
                    with open('./client_status.txt', 'r') as f:
                        print(__name, 'sending status to server.')
                        self.client_send(''.join(f.readlines()))
                except Exception as e:
                    print(__name, e)
