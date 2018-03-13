from wateralarm_client import MySocketClient

if __name__ == "__main__":
    """run this file to start the client. must have "client_status.txt" file
    which contains ID,alarm-status,sensor-status in format of 'xxx,x,x'.
    mySocket arguments:
        1. IP address of the server (host).
        2. the port number, which the server listens to
        3. Keep-Alive message. should be consistent with server "py" file.
           should be 'KA'."""
    client_socket = MySocketClient('localhost', 5432, 'KA')
    client_socket.run_client()
