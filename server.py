from wateralarm_server import MySocketServer

if __name__ == "__main__":
    """This server features:
    1. accepts connections on a secluded thread, thus -
    2. supports multi-clients connections.
    3. dynamically detects additional connections(from clients) and aborted connections.
    4. assumes a message from client of the form 'xxx,x,x'(of msg_len=7) form, for ID,alarm status
     water-sensor status.
    5. Make sure 'path_to_db' points to valid path"""
    server_socket = MySocketServer(5432, msg_len=7)
    path_to_db = 'C:/Users/Yehezkel/PycharmProjects/Python-Practice/data.db'
    server_socket.run_server(path_to_db)
