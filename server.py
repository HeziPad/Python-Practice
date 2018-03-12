import threading
from wateralarm_server import mySocket_server

if __name__ == "__main__":
    """This server features:
    1. accepting connections on a secluded thread, an thus
    2. supports multi-clients connections.
    3. dynamicly detecting addtional clients and aborted connections.
    4. assumes a message from client of the form 'xxx,x,x' form, for ID,alarm status
     water-sensor status."""
    server_socket = mySocket_server(5432,msg_len=7)
    path_to_db = 'C:/Users/Yehezkel/PycharmProjects/RTproject/venv/Scripts/data.db'
    server_socket.run_server(path_to_db)
