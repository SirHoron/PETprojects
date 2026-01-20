import socket
import sqlite3
import threading
from uuid import uuid4
from queue import Queue

connect = sqlite3.Connection("maindb.db", check_same_thread=False)
cursor = connect.cursor()

answer = {}
keys = {"ответ":"q98wd4v489hb16sdv984tb16","запрос на выполнение":"vte84a35fv4rg654asf8v68r4g","ошибка":"b984rtb1fv1b9ts1b953sd15bt"}

def handler(client, data):
    commands = {"new": new, "get": get, "delete": delete, "update": update}
    if data[len(data)-2] == keys["запрос на выполнение"]:
        try:
            msg = f"{data[0]}/{commands[data[1]](client, data[2])}/{keys['ответ']}/{data[len(data)-1]}"
            client.send(msg.encode())
            print(msg)
        except Exception as e:
            client.send(f"{data[0]}/DB:{e}/{keys["ошибка"]}/None".encode())
    elif data[len(data)-2] == keys["ответ"]:
        answer.update({data[len(data)-1]:data[0]})
    

def update(client:socket.socket, msg: str):
    pseudonym, userid = msg.split("|")
    key = uuid4()
    reqv = """ UPDATE Users SET pseudonym = ? WHERE userid = ? """ 
    cursor.execute(reqv, (pseudonym,int(userid)))
    connect.commit()
    client.send(f"cache/update/{pseudonym}|{userid}/{keys["запрос на выполнение"]}/{key}".encode())
    while True:
        answ = answer.get(key)
        if answ:
            return answ

def new(_, data):
    username,pseudonym,userid = data.split("|")
    if get(userid) == "None":
        reqv = """ INSERT INTO Users username,pseudonym,userid VALUES (?,?,?) """ 
        cursor.execute(reqv, (username,pseudonym,int(userid)))
        connect.commit()
        return "True"
    else:
        "Такой User уже существует"

def get(_, key):
    reqv = """SELECT username,pseudonym,userid FROM Users WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(reqv, (key, key, key))
    data = cursor.fetchall()
    print(data)
    if data:
        data = list(data[0])
        data[2] = str(data[2])
        data = "|".join(data)
        return data
    return "None"

def delete(_, key):
    reqv = """SELECT id FROM Users WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(reqv, (key, key, key))
    data = cursor.fetchall()
    reqv = """ DELETE FROM Users WHERE id = ? """
    cursor.execute(reqv, (data[0][0],))
    connect.commit()
    return "True"

def main():
    client = socket.socket()
    client.connect(("127.0.0.1", 56237))
    print("[Command log] Подключение установлено")
    queue = Queue(1000)
    thrd = threading.Thread()
    client.send(b"DB")
    while True:
        try:
            data = client.recv(2048).decode().split("/")
        except ConnectionResetError as e:
            print(e)
            break
        except socket.timeout:
            data = "g9rev49e6r6165wf1wev9rwg45df4g6"
        if data:
            print(data)
            if data[0] == "deactivate DB" or data[0] == "deactivate all":
                break
            if data != "g9rev49e6r6165wf1wev9rwg45df4g6":
                queue.put(data)
            if not thrd.is_alive() and not queue.empty():
                thrd = threading.Thread(target=handler, args=(client,  queue.get()), daemon=True)
                thrd.start()

if __name__ == "__main__":
    main()
    

    connect.close()
    print("DB завершил работу")