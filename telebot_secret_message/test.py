import socket
import asyncio
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("127.0.0.1", 12345))

while True:
    server.send(b'200')