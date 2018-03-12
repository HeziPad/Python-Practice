#!bin\python
import datetime
import socket as s
import threading
import time
from wateralarm_sql import water_alarm_sql

class mySocket_server(s.socket,water_alarm_sql):
    """Special designed class for Water-Stations-Alarm project,
    server-side. Inherits from custom SQL class"""
    def __init__(self, port, ip='', set_timeout=None, msg_len=7):
        s.socket.__init__(self)
        self.port = port
        self.ip = ip if ip != '' else ''
        if set_timeout is not None: self.set_timeout(set_timeout) #set global timeout, optional
        self.msg_len = msg_len if msg_len != 0 else 0 # Pre-known length of message from clients
        self._ka_time = 60 # time to send KA message
        self.clients = [] # Dynamic array which contains live and responding clients

    def run_server(self, path_to_db):
        """execute this function to run server.
        starts my_accept thread, and server_handler.
        path_to_db have to lead to .db sql file (will create a new file if not exists)"""
        __name = '[run_server]'
        with self:
            self.bind((self.ip, self.port))
            self.listen(5)
            threads = []
            INITIAL_THREADS = threading.active_count()
            print('creating accept thread')
            threads.append(threading.Thread(target=self.my_accept, name='Accept-Connections'))
            print('thread {} created'.format(threads[-1].name))
            print('creating clients handler thread')
            threads.append(threading.Thread(target=self.server_handler, name='Server-Handler',
                                            args=(path_to_db,)))
            print('thread {} created'.format(threads[-1].name))
            for each in threads:
                print('Starting', each.name)
                each.start()
            for each in threads:
                each.join()
                print(' thread joined', each.name)

    def my_accept(self):
        """Recieves new clients. functions on a secluded thread. each detected client is added
        to 'clients' list (socket object)"""
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
        """responsible for sending 'KA' messages to all clients. Unresponsive
        clients are removed from 'clients' list"""
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
                        except ConnectionAbortedError as e:
                            print(__name, 'removing client:', client, e)
                            del self.clients[index]
                            break
                time.sleep(self._ka_time)
            time.sleep(1)

    def server_receive(self,client_socket):
        """recieves messages from clients. messages must be of length 'msg_len'"""
        __name = '[server_receive]'
        chunks = []
        bytes_rcvd = 0
        while bytes_rcvd < self.msg_len:
            chunk = client_socket.recv(min(self.msg_len - bytes_rcvd, 2048)).decode()
            if chunk == '':
                raise ConnectionError(__name, "socket connection broken")
            bytes_rcvd = bytes_rcvd + len(chunk)
            if len(chunk) > 7:
                print(__name,'message too big from client: {}'.format(client_socket))
                chunk = ''
            else:
                chunks.append(chunk)
        return ''.join(chunks)

    def server_handler(self, path):
        """server handler. Starts keep-alive messaging thread. Recieves all messages and
        writes accordingly in SQL database. removes clients if client is unresponsive."""
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
                rcvd_data = []
                for client in [i[0] for i in self.clients]:
                    try:  # checks if client exists
                        print(__name, 'number of active clients: {}'.format(len(self.clients)))
                        rcvd_data.append(self.server_receive(client).split(sep=','))
                        sql.replace_row(rcvd_data[-1][0], datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                                             rcvd_data[-1][1],rcvd_data[-1][2])
                        sql.show_table()
                    except self.timeout:
                        print(__name, 'connection timed out!')
                        break
                    except Exception as e:
                        print(e)
                        break
                    except ConnectionError as e:
                        print(__name, 'msg time out! removing client {}.', client)
                        self.clients.remove(client)
                        break
                    finally:
                        time.sleep(self._ka_time)
                        break
            if print_once == 0:
                print(__name, 'no clients yet. Waiting...')
                print_once = 1
            time.sleep(1)
