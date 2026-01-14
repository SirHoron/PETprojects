import socket
import asyncio
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("127.0.0.1", 56237))
server.send(b"test")

while True:
    msg = input()
    server.send(msg.encode())
    while True:
        data = server.recv(1024)
        if data:
            print(data)
            break