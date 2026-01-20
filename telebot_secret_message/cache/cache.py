import sqlite3
import socket
from queue import Queue
import threading
from time import time
from uuid import uuid4

connect = sqlite3.Connection("cache.db", check_same_thread=False)
cursor = connect.cursor()

keys = {"ответ":"q98wd4v489hb16sdv984tb16", "запрос на выполнение":"vte84a35fv4rg654asf8v68r4g", "ошибка":"b984rtb1fv1b9ts1b953sd15bt"}

answer = {}

timer = {}

flage_thrd = False
flage = True

def delete(key):
    reqv = """ DELETE FROM Cache WHERE userid = ? """
    cursor.execute(reqv, (key))
    connect.commit()

def update(s, data: str):
    global timer
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
    global answer, flage_thrd
    search = """SELECT username,pseudonym,userid FROM Cache WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(search, (data, data, data))
    users = cursor.fetchall()
    if users:
        timer.update({users[0][2]:time()})
        return "True"
    else:
        key = uuid4()
        print(key)
        s.send(f"DB/get/{data}/{keys['запрос на выполнение']}/{key}".encode())
        while True:
            answ = answer.get(key)
            if answ != "None" and answ:
                answ.split("|")
                new(*answ)
                timer.update({answ[2]:time()})
                return "True"
            else:
                return "False"

def get(s, data):
    global answer
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
        key = uuid4()
        print(key)
        s.send(f"DB/get/{data}/{keys['запрос на выполнение']}/{key}".encode())
        while True:
            answ = answer.get(key)
            if answ != "None" and answ:
                answ = answ.split("|")
                new(*answ)
                timer.update({answ[2]:time()})
                return answ
                

def handler(s, data):
    global answer
    functions = {"get": get, "check": check, "new": new, "update": update}
    data1 = data.split("/")
    if data1[len(data1)-2] == keys["запрос на выполнение"]:
        reqv = functions[data1[1]](s, data1[2])
        s.sendall(f'{data1[0]}/{reqv}/{keys["ответ"]}/{data1[len(data1)-1]}'.encode())
        print("handler:",reqv)

def ttl():
    global timer, flage
    flage = False
    while True:
        if timer:
            newtime = time()
            for item in timer.keys():
                if newtime - timer[item] >= 600.0: 
                    delete(int(item))
                    timer.pop(item)
        flage = True

def main():
    global flage_thrd, flage, answer
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
                print(data)
            except socket.timeout:
                data = "g9rev49e6r6165wf1wev9rwg45df4g6"
            if data:
                if data == "deactivate all" or data == "deactivate cache":
                    break
                else:
                    spltdata = data.split("/")
                    if data != "g9rev49e6r6165wf1wev9rwg45df4g6":
                        newqueue.put(data)
                    if not thrd.is_alive() and not newqueue.empty() and flage:
                        info = newqueue.get()
                        thrd = threading.Thread(target=handler, args=(s, info), daemon=True)
                        thrd.start()
                        flage_thrd = False
                    if spltdata[len(spltdata)-2] == keys["ответ"]:
                        print('ответ')
                        answer.update({spltdata[len(spltdata)-1]:spltdata[0]})

    cursor.execute("""DELETE FROM Cache""")
    connect.commit()
    print("Cache очищен")
    connect.close()
    print("Cache завершил работу")


if __name__ == "__main__":
    main()
