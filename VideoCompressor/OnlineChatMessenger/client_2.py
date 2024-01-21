import socket
import threading
import time

def receive_messages(sock):
    while True:
        try:
            data, address = sock.recvfrom(4096)
            if data:
                friend_name_len = data[0]
                friend_name = data[1:1+friend_name_len].decode()
                friend_message = data[1+friend_name_len:].decode()
                print('{}: {}'.format(friend_name, friend_message))
        except socket.timeout:
            # タイムアウトした場合、ループを続ける
            continue

def send_messages(sock, server_address, my_name, usernamelen):
    while True:
        my_message = input("{}: ".format(my_name))
        data = usernamelen.to_bytes(1, 'big') + my_name.encode() + my_message.encode()
        sock.sendto(data, server_address)

my_name = input('What is your user name?\n')
usernamelen = len(my_name)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(30)  # ソケットのタイムアウトを30秒に設定
server_address = ('127.0.0.1', 9002)

# スレッドでメッセージの受信を開始
threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

# メッセージの送信
send_messages(sock, server_address, my_name, usernamelen)
