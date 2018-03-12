from wateralarm_client import mySocket_client

if __name__ == "__main__":
    client_socket = mySocket_client('localhost',5432,'KA')
    client_socket.run_client()