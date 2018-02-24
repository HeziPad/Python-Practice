from wateralarm import mySocket


if __name__ == "__main__":
    ka_msg = 'KA'
    with mySocket() as client_socket:
        print('connecting...')
        client_socket.connect(('localhost', 5432))
        print('connected!')
        client_socket.client_handler(ka_msg)
