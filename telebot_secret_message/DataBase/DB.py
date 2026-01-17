import socket
import sqlite3


connect = sqlite3.Connection("maindb.db")
cursor = connect.cursor()


def new(username,pseudonym,userid):
    if not get(userid):
        reqv = """ INSERT INTO Users username,pseudonym,userid VALUES (?,?,?) """ 
        cursor.execute(reqv, (username,pseudonym,userid))
        connect.commit()
        return "True"
    else:
        "Такой User уже существует"

def get(key):
    reqv = """SELECT username,pseudonym,userid FROM Users WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(reqv, (key, key, key))
    data = cursor.fetchall()
    if data:
        data = "|".join(data[0])
        return data
    return "None"

def delete(key):
    reqv = """SELECT id FROM Users WHERE username = ? or pseudonym = ? or userid = ?"""
    cursor.execute(reqv, (key, key, key))
    data = cursor.fetchall()
    reqv = """ DELETE FROM Users WHERE id = ? """
    cursor.execute(reqv, (data[0][0],))
    connect.commit()
    return True

if __name__ == "__main__":
    commands = {"new": new, "get": get, "delete": delete}
    client = socket.socket()
    client.connect(("127.0.0.1", 56237))
    client.send(b"DB")
    while True:
        data = client.recv(1024).decode().split("/")
        if data:
            if data[0] == "deactivat db" or data[0] == "deactivate all":
                break
            client.send(f"{data[0]}.{commands[data[1](data[2])]}.{data[3]}")
    connect.close()
    print("DB завершил работу")