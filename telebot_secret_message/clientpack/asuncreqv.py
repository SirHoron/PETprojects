import socket
import threading
from time import time
from uuid import uuid4

flage_1 = True
keys = {"ответ":"q98wd4v489hb16sdv984tb16","запрос на выполнение":"vte84a35fv4rg654asf8v68r4g","ошибка":"b984rtb1fv1b9ts1b953sd15bt"}
answer = {}

def handler(serv: socket.socket):
    global answer
    while True:
        try:
            data = serv.recv(2048).decode().split("/")
            print(data)
        except socket.timeout:
            continue
        if data[len(data)-2] == keys["ответ"]:
            print(data[len(data)-1])
            answer.update({data[len(data)-1]: data[0]})

try:
    client = socket.socket()
    client.connect(("127.0.0.1", 56237))
    print("[Command log] Подключение установлено")
    client.settimeout(0.1)
    threading.Thread(target=handler, kwargs={"serv":client}, daemon=True).start()
    client.send(b"main")
except Exception as e:
    print(e, "\n",
        f"{"---"*40}", "\n"
        "[Command log] Проверьте подключение контроллера")
    flage_1 = False

async def update(pseudonym,userid):
    global answer
    key = uuid4()
    msg = f"DB/update/{pseudonym}|{userid}/{keys['запрос на выполнение']}/{key}"
    client.send(msg.encode())
    print(msg)
    start = time()
    while True:
        end = time()
        answ = answer.get(key)
        if answ:
            answer.pop(key)
            return answ
        if end-start>3:
            print("время ожидания вышло")
            return "время ожидания вышло"

async def new(username,pseudonym,userid):
    global answer
    key = uuid4()
    msg = f"DB/new/{username}|{pseudonym}|{userid}/{keys['запрос на выполнение']}"
    client.send(msg.encode())
    print(msg)
    start = time()
    while True:
        end = time()
        answ = answer.get(key)
        if answ:
            answer.pop(key)
            return answ
        if end-start>3:
            print("время ожидания вышло")
            return "время ожидания вышло"

async def get(data):
    global answer
    key = uuid4()
    msg = f"cache/get/{data}/{keys['запрос на выполнение']}"
    client.send(msg.encode())
    print(msg)
    start = time()
    while True:
        end = time()
        answ = answer.get(key)
        if answ:
            answer.pop(key)
            return answ.split("|")
        if end-start >= 3:
            print("время ожидания вышло")
            return "время ожидания вышло"
        

async def check(name):
    global answer
    key = uuid4()
    answ1 = {"True": True, "False": False}
    msg = f"cache/check/{name}/{keys['запрос на выполнение']}/{key}"
    client.send(msg.encode())
    print(msg)
    start = time()
    while True:
        end = time()
        print(answer)
        answ = answer.get(key)
        if answ:
            answer.pop(key)
            return answ1.get(answ)
        if end-start>3:
            print("время ожидания вышло")
            return "время ожидания вышло"