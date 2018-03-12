import threading
from wateralarm_server import mySocket_server

if __name__ == "__main__":
    server_socket = mySocket_server(5432)
    path_to_db = 'C:/Users/Yehezkel/PycharmProjects/RTproject/venv/Scripts/data.db'
    server_socket.run_server(path_to_db)
