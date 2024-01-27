import socket

def main():
    host = '127.0.0.1'  # ローカルホスト
    port = 65432        # 非特権ポート

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                response = f"クライアントからのテキスト「{data.decode()}」を受け取りました！"
                conn.sendall(response.encode())

if __name__ == "__main__":
    main()
