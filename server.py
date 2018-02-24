import threading
from wateralarm import mySocket

if __name__ == "__main__":
    with mySocket(msg_len=7) as server_socket:
        server_socket.bind(('', 5432))
        server_socket.listen(5)
        threads = []
        INITIAL_THREADS = threading.active_count()
        print('creating accept thread')
        threads.append(threading.Thread(target=server_socket.my_accept, name='Accept-Connections'))
        print('Thread {} created'.format(threads[-1].name))
        print('creating clients handler thread')
        threads.append(threading.Thread(target=server_socket.server_handler, name='Server-Handler',
                                        args=('C:/Users/Yehezkel/PycharmProjects/RTproject/venv/Scripts/data.db',)))
        print('Thread {} created'.format(threads[-1].name))
        for each in threads:
            print('Starting', each.name)
            each.start()
        for each in threads:
            each.join()
            print(' thread joined', each.name)
