import socket

# AF_INETを使用し、UDPソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001
print('starting up on port {}'.format(server_port))

# ソケットを特殊なアドレス0.0.0.0とポート9001に紐付け
sock.bind((server_address, server_port))

while True:
   print('\nwaiting to receive message')
   data, address = sock.recvfrom(4096)

   print('received {} bytes from {}'.format(len(data), address))
   print(data)

   if data:
       sent = sock.sendto(data, address)
       print('sent {} bytes back to {}'.format(sent, address))