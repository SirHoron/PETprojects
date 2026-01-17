import socket

help = \
"""

"""

with socket.socket() as client:
    client.connect(("127.0.0.1", 56237))
    print("[Command log] Подкючение успешно")
    client.send(b"admin:r4wb98t4yb5a4etb8t4b6erg4*$94fr)")
    while True:
        msg = input("Введите сообщение контроллеру:")
        if msg == "help":
            print(help)
            continue
        if len(msg.split("/")) == 4:
            client.send(msg.encode())
            continue
        if msg == "deactivate all":
            client.send(msg.encode())
            break
        elif "deactivate" in msg:
            client.send(msg.encode())

print("Работа завершена")