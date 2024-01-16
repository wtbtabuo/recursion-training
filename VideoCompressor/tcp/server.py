from faker import Factory
import socket
import os


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = 'socket_file'

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print('Starting up on {}'.format(server_address))

sock.bind(server_address)

sock.listen(1)

fake_jp = Factory.create()
faker_methods = {
    'name': fake_jp.name,
    'address': fake_jp.address,
    'email': fake_jp.email
}

while True:
    connection, client_address = sock.accept()
    try:
        print('connected')

        while True:
            data = connection.recv(16)
            data_str = data.decode('utf-8').strip()

            if data:
                if data_str in faker_methods:
                    res = faker_methods[data_str]()
                    connection.sendall(res.encode())
                else:
                    connection.sendall("invalid method".encode())

            else:
                print('no data from', client_address)
                break

    finally:
        print("Closing current connection")
        connection.close()