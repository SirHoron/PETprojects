import socket
import threading
from queue import Queue

"""
    мы получаем 'куда/команда для выполнения/данные(если много то разделяется '|')/ключ' len = 4

    [] мы отправляем 'от кого был запрос/команда для выполнения/данные(если много то разделяется '|')/ключ' len = 4

    мы получаем в ответ 'от кого был запрос/ответ или ошибка(если много то разделяется '|')/ключ' len = 3

    [] мы отправляем ответ 'ответ или ошибка(если много то разделяется '|')/ключ' len = 2
"""

keys = {"ответ":"q98wd4v489hb16sdv984tb16","запрос на выполнение":"vte84a35fv4rg654asf8v68r4g","ошибка":"b984rtb1fv1b9ts1b953sd15bt"}

clients: dict[str, list[socket.socket]] = {}
flage = True

def handler(con: socket.socket, name, data):
    global flage
    data = data.split("/")
    lendata = len(data)
    print(data)
    if name == "admin:r4wb98t4yb5a4etb8t4b6erg4*$94fr)":
        if data[0] == "deactivate all":
            for i in clients.values():
                i[0].send(b"deactivate all")
            flage = False
            con.close()
        elif data[0] == "deactivate cache":
            if "cache" in clients.keys():
                clients["cache"][0].send(b"deactivate cache")
                clients["cache"][0].close()
        elif data[0] == "deactivate DB":
            if "DB" in clients.keys():
                clients["DB"][0].send(b"deactivate DB")
                clients["DB"][0].close()
        elif data[0] == "deactivate":
            flage = False
    if data[lendata-2] == keys["запрос на выполнение"] and lendata == 5:
        reqv = f"{name}/{data[1]}/{data[2]}/{keys['запрос на выполнение']}/{data[lendata-1]}"
        clients[data[0]][0].send(reqv.encode())
    if (data[lendata-2] == keys["ответ"] or data[lendata-2] == keys["ошибка"]) and lendata == 4:
        reqv = f"{data[1]}/{data[2]}/{data[lendata-1]}"
        print(reqv)
        clients[data[0]][0].send(reqv.encode())
        print(data[0])

def client_thread(con: socket.socket, name):
    global clients
    con.settimeout(0.1)
    newqueue = Queue(1000)
    thrd = threading.Thread()
    while True:
        try:
            data1 = con.recv(2048).decode()
        except ConnectionAbortedError as e:
            clients.pop(name)
            print(e)
            break
        except ConnectionResetError as e:
            clients.pop(name)
            con.close()
            print(e)
            break
        except socket.timeout:
            data1 = "g9rev49e6r6165wf1wev9rwg45df4g6"
        if data1:
            if data1 != "g9rev49e6r6165wf1wev9rwg45df4g6":
                newqueue.put(data1)
            if not thrd.is_alive() and not newqueue.empty():
                thrd = threading.Thread(target=handler, args=(con, name,  newqueue.get()), daemon=True)
                thrd.start()
        else:
            con.close()
            break

def main():
    server = socket.socket()
    server.bind(("127.0.0.1", 56237))
    server.listen(5)
    server.settimeout(0.1)
    print("Server running")
    while flage:
        try:
            client, _ = server.accept()
        except socket.timeout:
            continue
        while True:
            try:
                data = client.recv(1024)
            except socket.timeout:
                continue
            clients.update({data.decode(): [client, "0"]})
            break
        thrd = threading.Thread(target=client_thread, args=(client, data.decode()), daemon=True)
        thrd.start()
        print(data.decode())
    server.close()
    print("Controller завершил работу")

if __name__ == "__main__":
    main()