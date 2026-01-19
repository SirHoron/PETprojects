import sqlite3
import socket
from queue import Queue
import threading
from time import time

connect = sqlite3.Connection("cache.db", check_same_thread=False)
cursor = connect.cursor()

keys = {"ответ":"q98wd4v489hb16sdv984tb16", "запрос на выполнение":"vte84a35fv4rg654asf8v68r4g", "ошибка":"b984rtb1fv1b9ts1b953sd15bt"}

timer = {}

flage = True

def ttl():
    global timer, flage
    flage = False
    while True:
        if timer:
            newtime = time()
            for item in timer.keys():
                if newtime - timer[item] >= 600.0: 
                    timer.pop(item)
        flage = True

def update(s, data: str):
    pseudonym, userid = data.split("|")
    reqv = """ UPDATE Cache SET pseudonym = ? WHERE userid = ? """ 
    try:
        cursor.execute(reqv, (pseudonym,int(userid)))
        timer.update({userid:time()})
    except sqlite3.OperationalError:
        pass
    connect.commit()
    return "True"

def new(username: str, pseudonym: str, userid: int):
    reqv = """INSERT INTO Cache (username, pseudonym, userid) VALUES (?,?,?)"""
    cursor.execute(reqv, (username, pseudonym, int(userid)))
    connect.commit()
    timer.update({userid:time()})
    

def check(s, data) -> bool:
    search = """SELECT username,pseudonym,userid FROM Cache WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(search, (data, data, data))
    users = cursor.fetchall()
    if users:
        timer.update({users[0][2]:time()})
        return "True"
    else:
        if get(s, data):
            timer.update({users[0][2]:time()})
            return "True"
        else:
            return "False"

def get(s, data):
    search = """SELECT username,pseudonym,userid FROM Cache WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(search, (data,data,data))
    user = cursor.fetchall()
    if user:
        timer.update({user[0][2]:time()})
        user = list(user[0])
        user[2] = str(user[2])
        user = "|".join(user)
        return user
    else:
        s.send(f"DB/get/{data}/{keys['запрос на выполнение']}".encode())
        while True:
            try:
                data1 = s.recv(2048).decode().split("/")
                if data1:
                    if data1[1] == keys["ответ"] and data1[0] != "None":
                        new(*data1[0].split("|"))
                        return data1[0]
                    break 
            except socket.timeout:
                pass
                

def handler(s, data):
    functions = {"get": get, "check": check, "new": new, "update": update}
    data1 = data.split("/")
    if data1[len(data1)-1] == keys["запрос на выполнение"]:
        try:    
            reqv = functions[data1[1]](s, data1[2])
            s.sendall(f'{data1[0]}/{reqv}/{keys["ответ"]}'.encode())
        except Exception as e:
            print(e)
            msg = f"{data[0]}/cache:{e}/{keys['ошибка']}"
            s.sendall(f'{msg}'.encode())
    else:
        print(data1)


def main():
    with socket.socket() as s:
        s.connect(("127.0.0.1", 56237))
        print("[Command log] Подключение установлено")
        s.send(b"cache")
        s.settimeout(0.2)
        newqueue = Queue(10000)
        threading.Thread(target=ttl, daemon=True).start()
        thrd = threading.Thread()
        while True:
            try:
                data = s.recv(2048).decode()
            except socket.timeout:
                data = "g9rev49e6r6165wf1wev9rwg45df4g6"
            if data:
                if data == "deactivate all" or data == "deactivate cache":
                    break
                else:
                    if data != "g9rev49e6r6165wf1wev9rwg45df4g6":
                        newqueue.put(data)
                    if not thrd.is_alive() and not newqueue.empty() and flage:
                        info = newqueue.get()
                        print(info)
                        thrd = threading.Thread(target=handler, args=(s, info), daemon=True)
                        thrd.start()

    cursor.execute("""DELETE FROM Cache""")
    connect.commit()
    print("Cache очищен")
    connect.close()
    print("Cache завершил работу")


if __name__ == "__main__":
    main()
