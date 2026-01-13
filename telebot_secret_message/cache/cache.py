import sqlite3
import socket

connect = sqlite3.Connection("cache.db")
cursor = connect.cursor()

def check(name) -> bool:
    search = """SELECT username,pseudonym FROM Cache"""
    cursor.execute(search)
    names = cursor.fetchall()
    for i in names:
        if name in i:
            return True
    return False

def get(key) -> tuple:
    search = """SELECT username,pseudonym,userid FROM Cache"""
    cursor.execute(search)
    users = cursor.fetchall()
    for i in range(len(users)):
        if key in users[i]:
            return users[i]
    return ()

if __name__ == "__main__":
    functions = {"get": get, "check":check}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 12345))
        print("[Command log] Подключение установлено")
        while True:
            data = s.recv(1024)
            if data:
                data = data.decode().split(".")
                try:
                    msg = functions[data[0]](data[1])
                    s.sendall(f'{msg}'.encode())
                except KeyError:
                    s.sendall(b'This command does not exist or is entered incorrectly.')
        connect.close()