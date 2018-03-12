#!bin\python
import datetime
import socket as s
import threading
import time
from wateralarm_sql import water_alarm_sql

class mySocket_server(s.socket,water_alarm_sql):
    """Special designed class for Water-Stations-Alarm project"""
    def __init__(self, port, ip='', set_timeout=None, msg_len=0):
        s.socket.__init__(self)
        self.port = port
        self.ip = ip if ip != '' else ''
        if set_timeout is not None: self.set_timeout(set_timeout)
        self.msg_len = msg_len if msg_len != 0 else 0
        self._ka_time = 15
        self.clients = []

    def run_server(self, path_to_db):
        with self:
            self.bind((self.ip, self.port))
            self.listen(5)
            threads = []
            INITIAL_THREADS = threading.active_count()
            print('creating accept thread')
            threads.append(threading.Thread(target=self.my_accept, name='Accept-Connections'))
            print('thread {} created'.format(threads[-1].name))
            print('creating clients handler thread')
            threads.append(threading.Thread(target=self.server_handle_clients, name='Server-Handler',
                                            args=(path_to_db,)))
            print('thread {} created'.format(threads[-1].name))
            for each in threads:
                print('Starting', each.name)
                each.start()
            for each in threads:
                each.join()
                print(' thread joined', each.name)

    def my_accept(self):
        """Recieves new clients."""
        __name = '[my_accept]'
        print_once = 0
        while True:
            try:
                if print_once == 0:
                    print(__name, 'Waiting for client connection...')
                    print_once = 1
                (client_socket, (address, port)) = self.accept()
                print_once = 0
                print(__name, 'ACCEPTED IP:{}'.format(address))
                if any(address in  sublist for sublist in self.clients) is True:
                    print(__name, 'client already exists!')
                else:
                    print(__name, 'A new client connected! IP:{} Port:{}'.format(address,port))
                    self.clients.append([client_socket,
                                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            except Exception as e:
                print(__name, e)
                pass

    def server_sendtoall(self, msg='KA'):
        __name = '[server_sendtoall]'
        while True:
            while len(self.clients) > 0:
                for index,client in enumerate(each[0] for each in self.clients):
                    totalsent = 0
                    while totalsent < len(msg):
                        try:
                            sent = client.send(msg[totalsent:].encode())
                            if sent == 0:
                                raise RuntimeError(__name, "socket connection broken")
                            totalsent = totalsent + sent
                        except ConnectionResetError as e:
                            print(__name, 'removing client:',client,e)
                            del self.clients[index]
                            break
                time.sleep(self._ka_time)
            time.sleep(1)

    def server_receive(self,client_socket):
        __name = '[server_receive]'
        chunks = []
        bytes_rcvd = 0
        while bytes_rcvd < self.msg_len:
            chunk = client_socket.recv(min(self.msg_len - bytes_rcvd, 2048)).decode()
            if chunk == '':
                raise RuntimeError(__name, "socket connection broken")
            chunks.append(chunk)
            bytes_rcvd = bytes_rcvd + len(chunk)
        return ''.join(chunks)

    def server_handle_clients(self, path):
        __name = '[server_handler]'
        sql = water_alarm_sql(path)
        print_once = 0
        print(__name, 'starting keep-alive thread.')
        ka_thread = threading.Thread(target=self.server_sendtoall,name='keep-alive thread')
        ka_thread.start()
        print(__name, 'keep-alive thread started')
        while True:
            while len(self.clients) > 0:
                print_once = 0
                try:  # checks if client exists
                    rcvd_data = []
                    for client in [i[0] for i in self.clients]:
                        rcvd_data.append(self.server_receive(client))#.split(sep='\n'))
                        sql.replace_row(rcvd_data[-1][0], datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                                             rcvd_data[-1][1],rcvd_data[-1][2])
                        sql.show_table()
                except self.timeout:
                    print(__name, 'connection timed out!')
                except Exception as e:
                    print(e)
                finally:
                    time.sleep(self._ka_time)
            if print_once == 0:
                print(__name, 'no clients yet. Waiting...')
                print_once = 1
            time.sleep(1)
