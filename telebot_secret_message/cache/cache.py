import sqlite3
import socket

connect = sqlite3.Connection("cache.db")
cursor = connect.cursor()

"""
    Форма запроса 'метод.[данные].кодзадачи'
    Форма ответа 'кодзадачи.ответ|кодошибки'
"""


def new(username: str, pseudonym: str, userid: int):
    reqv = """INSERT INTO Cache (username, pseudonym, userid) VALUES (?,?,?)"""
    cursor.execute(reqv, (username, pseudonym, userid))
    connect.commit()

def check(name) -> bool:
    search = """SELECT username,pseudonym,userid FROM Cache WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(search, (name, name, name))
    name = cursor.fetchall()
    if name:
        return "True"
    return "False"

def get(key):
    search = """SELECT username,pseudonym,userid FROM Cache WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(search, (key,key,key))
    user = cursor.fetchall()
    if user:
        user = list(user[0])
        user[2] = str(user[2])
        user = "|".join(list(user))
        return user
    else:
        s.send(f"DB/get/{key}/12f3d4ht5".encode())
        while True:
            data = s.recv(1024).decode().split("/")
            if data and data[2] == "12f3d4ht5":
                data = "|".join(data[1])
                return data
                

if __name__ == "__main__":
    functions = {"get": get, "check": check, "new": new}
    with socket.socket() as s:
        s.connect(("127.0.0.1", 56237))
        print("[Command log] Подключение установлено")
        s.send(b"cache")
        while True:
            data = s.recv(1024)
            if data:
                if data.decode() == "deactivate all" or data.decode() == "deactivate cache":
                    break
                if len(data.decode().split("/")) == 4:
                    try:
                        data = data.decode().split("/")
                        s.sendall(f'{data[0]}/{functions[data[1]](data[2])}/{data[3]}'.encode())
                    except Exception as e:
                        print(e)
                        msg = data[0] + "/" + f"{e}" + "/" + "N"
                        s.sendall(f'{msg}'.encode())
                else:
                    print(data.decode())
    connect.close()
    print("Cache завершил работу")
