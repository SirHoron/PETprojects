import socket
import sqlite3


connect = sqlite3.Connection("maindb.db")
cursor = connect.cursor()

keys = {"ответ":"q98wd4v489hb16sdv984tb16","запрос на выполнение":"vte84a35fv4rg654asf8v68r4g","ошибка":"b984rtb1fv1b9ts1b953sd15bt"}

def update(msg: str):
    pseudonym, userid = msg.split("|")
    reqv = """ UPDATE Users SET pseudonym = ? WHERE userid = ? """ 
    cursor.execute(reqv, (pseudonym,int(userid)))
    connect.commit()
    client.send(f"cache/update/{pseudonym}|{userid}/{keys["запрос на выполнение"]}".encode())
    if client.recv(512).decode() == "Yes":
        print("yes")
        return "True"

def new(username,pseudonym,userid):
    if get(userid) == "None":
        reqv = """ INSERT INTO Users username,pseudonym,userid VALUES (?,?,?) """ 
        cursor.execute(reqv, (username,pseudonym,int(userid)))
        connect.commit()
        return "True"
    else:
        "Такой User уже существует"

def get(key):
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

def delete(key):
    reqv = """SELECT id FROM Users WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(reqv, (key, key, key))
    data = cursor.fetchall()
    reqv = """ DELETE FROM Users WHERE id = ? """
    cursor.execute(reqv, (data[0][0],))
    connect.commit()
    return "True"

def main():
    commands = {"new": new, "get": get, "delete": delete, "update": update}
    while True:
        try:
            data = client.recv(2048).decode().split("/")
        except ConnectionResetError as e:
            print(e)
            break
        if data:
            print(data)
            if data[0] == "deactivate DB" or data[0] == "deactivate all":
                break
            if data[len(data)-1] == keys["запрос на выполнение"]:
                try:
                    while True:
                        msg = f"{data[0]}/{commands[data[1]](data[2])}/{keys['ответ']}"
                        client.send(msg.encode())
                        print(msg)
                        if client.recv(512).decode() == "Yes":
                            break
                except Exception as e:
                    client.send(f"{data[0]}/DB:{e}/{keys["ошибка"]}".encode())

if __name__ == "__main__":
    client = socket.socket()
    client.connect(("127.0.0.1", 56237))
    print("[Command log] Подключение установлено")
    client.send(b"DB")
    main()
    

    connect.close()
    print("DB завершил работу")