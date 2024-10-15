import os
import socket
from datetime import datetime

def save_request_to_file(response_data):
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'./request/{timestamp}.bin'
    
    with open(filename, 'wb') as file:
        file.write(response_data)

def main():
    if not os.path.exists('request'):
        os.makedirs('request')
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('127.0.0.1', 65432))
        server_socket.listen()
        print("Server is listening")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if data:
                    http_response = b"""HTTP/1.1 200 OK
Server: socket server v0.1
Content-Type: text/plain

<html>
<head>
<title>socket server</title>
</head>
<body>I've got your message</body>
</html>
"""
                    save_request_to_file(http_response)
                    conn.sendall(http_response)

if __name__ == "__main__":
    main()
