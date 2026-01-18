import sqlite3
import socket

connect = sqlite3.Connection("cache.db")
cursor = connect.cursor()

keys = {"ответ":"q98wd4v489hb16sdv984tb16","запрос на выполнение":"vte84a35fv4rg654asf8v68r4g","ошибка":"b984rtb1fv1b9ts1b953sd15bt"}

def update(data: str):
    pseudonym, userid = data.split("|")
    reqv = """ UPDATE Cache SET pseudonym = ? WHERE userid = ? """ 
    try:
        cursor.execute(reqv, (pseudonym,int(userid)))
    except sqlite3.OperationalError:
        pass
    connect.commit()
    return "True"

def new(username: str, pseudonym: str, userid: int):
    reqv = """INSERT INTO Cache (username, pseudonym, userid) VALUES (?,?,?)"""
    cursor.execute(reqv, (username, pseudonym, int(userid)))
    connect.commit()

def check(name) -> bool:
    search = """SELECT username,pseudonym,userid FROM Cache WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(search, (name, name, name))
    users = cursor.fetchall()
    if users:
        return "True"
    else:
        if get(name):
            return "True"
        else:
            return "False"

def get(key):
    search = """SELECT username,pseudonym,userid FROM Cache WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(search, (key,key,key))
    user = cursor.fetchall()
    if user:
        user = list(user[0])
        user[2] = str(user[2])
        user = "|".join(user)
        return user
    else:
        s.send(f"DB/get/{key}/{keys['запрос на выполнение']}".encode())
        while True:
            data = s.recv(1024).decode()
            if data == "Yes":
                break
        data = s.recv(1024).decode().split("/")
        if data:
            print(data)
            if data[1] == keys["ответ"] and data[0] != "None":
                new(*data[0].split("|"))
                return data[0]
                

if __name__ == "__main__":
    functions = {"get": get, "check": check, "new": new, "update": update}
    with socket.socket() as s:
        s.connect(("127.0.0.1", 56237))
        print("[Command log] Подключение установлено")
        s.send(b"cache")
        while True:
            data = s.recv(2048)
            if data:
                data = data.decode().split("/")
                print(data)
                if data[0] == "deactivate all" or data[0] == "deactivate cache":
                    break
                if data[len(data)-1] == keys["запрос на выполнение"]:
                    try:
                        while True:
                            s.sendall(f'{data[0]}/{functions[data[1]](data[2])}/{keys["ответ"]}'.encode())
                            if s.recv(512).decode() == "Yes":
                                break
                    except Exception as e:
                        print(e)
                        msg = f"{data[0]}/cache:{e}/{keys['ошибка']}"
                        s.sendall(f'{msg}'.encode())
                else:
                    print(data)
    cursor.execute("""DELETE FROM Cache""")
    connect.commit()
    connect.close()
    print("Cache завершил работу")
