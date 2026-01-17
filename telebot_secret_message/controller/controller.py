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
    global clients, flage
    while True:
        try:
            data = con.recv(1024)
        except ConnectionResetError as e:
            clients.pop(name)
            con.close()
            exit_thread()
            print(e)
            break
        if data:
            print(data)
            if name == "admin:r4wb98t4yb5a4etb8t4b6erg4*$94fr)":
                if data.decode() == "deactivate all":
                    for i in clients.values():
                        i[0].send(b"deactivate all")
                    server.close()
                    con.close()
                    exit_thread()
                    break
                elif data.decode() == "deactivate cache":
                    if "cache" in clients.keys():
                        clients["cache"][0].send(b"deactivate cache")
                        clients["cache"][0].close()
                elif data.decode() == "deactivate DB":
                    if "DB" in clients.keys():
                        clients["DB"][0].send(b"deactivate DB")
                        clients["DB"][0].close()
                elif data.decode() == "deactivate":
                    server.close()
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
        try:
            client, _ = server.accept()
        except OSError:
            break
        data = client.recv(1024)
        if data:
            clients.update({data.decode(): [client, "0"]})
        start_new_thread(client_thread, (client, data.decode()))
    print("Controller завершил работу")