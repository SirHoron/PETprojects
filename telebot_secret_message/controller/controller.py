import socket
from _thread import *

"""
    Форма запроса 'кому.метод.данные.кодзадачи'
    Форма отправки в cache 'откого.метод.данные.кодзадачи'
    Форма ответа от cache 'кому.ответ|кодошибки.кодзадачи'
    Форма ответа 'ответ|кодошибки.код+кодзадачи'
"""

clients: dict[str, list[socket.socket]] = {}

def client_thread(con: socket.socket, name):
    global clients
    while True:
        try:
            data = con.recv(1024)
        except ConnectionResetError as e:
            clients.pop(name)
            print(e)
        if data:
            try:
                data = data.decode().split("/")
                if len(data) == 3:
                    print("Yes")
                    msg = data[1] + "/" + "200" + data[2]
                    clients[data[0]][0].send(msg.encode())
                    print(msg)
                elif len(data) == 4:
                    msg: str = name + '/' + data[1] + "/" + data[2] + "/" + data[3]
                    clients[data[0]][1] = data[3]
                    clients[data[0]][0].send(msg.encode())
                    print(msg)
                else:
                    con.send(b"Incorrect form of the request")
                    print("Incorrect form of the request")
            except Exception as e:
                print(e)
                con.send(f"{e}".encode())

if __name__ == "__main__":
    server = socket.socket()
    server.bind(("127.0.0.1", 56237))
    server.listen(5)
    print("Server running")
    while True:
        client, _ = server.accept()
        data = client.recv(1024)
        if data:
            clients.update({data.decode(): [client, "0"]})
        start_new_thread(client_thread, (client, data.decode()))