import sqlite3
import socket

connect = sqlite3.Connection("cache.db")
cursor = connect.cursor()

"""
    Форма запроса 'метод.[данные].кодзадачи'
    Форма ответа 'кодзадачи.ответ|кодошибки'
"""

def check(name) -> bool:
    search = """SELECT username,pseudonym FROM Cache"""
    cursor.execute(search)
    names = cursor.fetchall()
    for i in names:
        if name in i:
            return "True"
    return "False"

def get(key) -> tuple:
    search = """SELECT username,pseudonym,userid FROM Cache"""
    cursor.execute(search)
    users = cursor.fetchall()
    answ = ""
    for i in range(len(users)):
        if key in users[i]:
            for i in users[i]:
                answ += str(i) + "|"
            return answ
    return "None"

if __name__ == "__main__":
    functions = {"get": get, "check":check}
    with socket.socket() as s:
        s.connect(("127.0.0.1", 56237))
        print("[Command log] Подключение установлено")
        s.send(b"cache")
        while True:
            data = s.recv(1024)
            if data:
                try:
                    data = data.decode()
                    data = data.split("/")
                    info: str = data[2]
                    msg = data[0] + "/" + functions[data[1]](info) + "/" + data[3]
                    s.sendall(f'{msg}'.encode())
                    print(msg)
                except Exception as e:
                    msg = data[0] + "/" + f"{e}" + "/" + "N"
                    s.sendall(f'{msg}'.encode())
        connect.close()