import socket

flage_1 = True

try:
    client = socket.socket()
    client.connect(("127.0.0.1", 56237))
    print("[Command log] Подключение установлено")
    client.settimeout(5)
    client.send(b"main")
except Exception as e:
    print(e, "\n",
        f"{"---"*40}", "\n"
        "[Command log] Проверьте подключение контроллера")
    flage_1 = False

keys = {"ответ":"q98wd4v489hb16sdv984tb16","запрос на выполнение":"vte84a35fv4rg654asf8v68r4g","ошибка":"b984rtb1fv1b9ts1b953sd15bt"}

async def update(pseudonym,userid):
    while True:
        msg = f"DB/update/{pseudonym}|{userid}/{keys['запрос на выполнение']}"
        client.send(msg.encode())
        if client.recv(2048).decode() == "Yes":
            break
    print(msg)
    try:
        data = client.recv(2048).decode().split('/')
    except socket.timeout:
        print(f"[Ошибка] время ожидания истекло")
        return None
    if data:
        if data[0] == "True":
            return True

async def new(username,pseudonym,userid):
    while True:
        msg = f"DB/new/{username}|{pseudonym}|{userid}/{keys['запрос на выполнение']}"
        client.send(msg.encode())
        if client.recv(2048).decode() == "Yes":
            break
    print(msg)
    try:
        data = client.recv(2048).decode().split('/')
    except socket.timeout:
        print(f"[Ошибка] время ожидания истекло")
        return None
    if data:
        if data[0] != "None" and data[1] != keys["ошибка"] and data[1] == keys["ответ"]:
            return True
        else:
            print(f"[Ошибка] {data}")

async def get(key):
    while True:
        msg = f"cache/get/{key}/{keys['запрос на выполнение']}"
        client.send(msg.encode())
        if client.recv(2048).decode() == "Yes":
            break
    print(msg)
    try:
        data = client.recv(2048).decode().split('/')
    except socket.timeout:
        print(f"[Ошибка] время ожидания истекло")
        return None
    if data:
        print(data)
        if data[0] != "None" and data[1] != keys["ошибка"] and data[1] == keys["ответ"]:
            data = data[0].split('|')
            data[2] = int(data[2])
            return data
        else:
            print(f"[Ошибка] {data}")
        

async def check(name):
    answ = {"True": True, "False": False}
    while True:
        msg = f"cache/check/{name}/{keys['запрос на выполнение']}"
        client.send(msg.encode())
        if client.recv(2048).decode() == "Yes":
            break
    print(msg)
    try:
        data = client.recv(2048).decode().split('/')
    except socket.timeout:
        print(f"[Ошибка] время ожидания истекло")
        return None
    if data and len(data) == 2:
        if data[1] != keys["ошибка"] and data[1] == keys["ответ"]:
            return answ[data[0]]
        else:
            print(f"[ошибка] {data}")
    else:
        print(f"[ошибка] {data}")