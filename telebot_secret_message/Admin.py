import socket
import time
help = \
"""

"""

keys = {"ответ":"q98wd4v489hb16sdv984tb16","запрос на выполнение":"vte84a35fv4rg654asf8v68r4g","ошибка":"b984rtb1fv1b9ts1b953sd15bt"}

with socket.socket() as client:
    client.connect(("127.0.0.1", 56237))
    print("[Command log] Подкючение успешно")
    client.settimeout(5)
    client.send(b"admin:r4wb98t4yb5a4etb8t4b6erg4*$94fr)")
    while True:
        msg = input("Введите сообщение контроллеру:")
        if msg == "help":
            print(help)
            continue
        if msg == "deactivate all":
            client.send(msg.encode())
            break
        elif "deactivate" in msg:
            client.send(msg.encode())
        if len(msg.split("/")) == 5:
            client.send(msg.encode())
            try:
                data = client.recv(2048)
                print(data)
            except socket.timeout:
                print("время ожидания вышло")

    time.sleep(1)

print("Работа завершена")