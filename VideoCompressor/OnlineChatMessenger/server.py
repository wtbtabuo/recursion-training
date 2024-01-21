import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = '127.0.0.1'
server_port = 9002

sock.bind((server_address, server_port))

clients = set()  # 接続されているクライアントのアドレスを保持

while True:
    data, address = sock.recvfrom(4096)
    clients.add(address)  # 新しいクライアントのアドレスを記録
    if data:
        for client in clients:
            if client != address:  # 送信元以外のクライアントにデータを転送
                sock.sendto(data, client)
