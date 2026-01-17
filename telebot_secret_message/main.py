from telebot import TeleBot
import socket
from uuid import uuid4
import asyncio

try:
    client = socket.socket()
    client.connect(("127.0.0.1", 56237))
    print("[Command log] Подключение установлено")
    client.send(b"main")
except Exception as e:
    print(e, "\n",
        f"{"---"*40}", "\n"
        "[Command log] Проверьте подключение контроллера")
    __name__ = "None"

bot = TeleBot("8403549969:AAGRdJvDRD5C8slSlMD2uzTaSwntu3MgHJw")

CommandOfId: dict[list] = {}

def get(key):
    client.send(f"cache/get/{key}/{uuid4()}".encode())
    while True:
        data = client.recv(1024).decode().split('/')
        if data:
            print(data)
            if data != "None" and len(data) == 3:
                data = data[0].split('|')
                data[2] = int(data[2])
                return data
        

def check(name):
    answ = {"True": True, "False": False}
    client.send(f"cache/check/{name}/{uuid4()}".encode())
    while True:
        data = client.recv(1024).decode().split('/')
        if data:
            print(data)
            return answ[data[0]]
        
class Commands:
    def send(self, reqv):
        print(reqv.text)
        message = f"""*Тебе анонимно написали:*
    {reqv.text}"""
        data = get(CommandOfId[reqv.chat.id][1])
        print(data)
        bot.send_message(data[2], message, parse_mode="Markdown")
        CommandOfId.pop(reqv.chat.id)
cmd = Commands()

@bot.message_handler(commands=["start"])
def start(reqv):
    print("gfv")
    bot.send_message(reqv.chat.id,
"""Приветствую Вас, я тестовый бот.
Я буду выполнять различные задачи, и для того чтобы узнать
какую мне дали задачу ныне, введите /help.""")

@bot.message_handler(commands=["help"])
def help(reqv):
    message = """
Данный бот предназначен для анонимной отправки сообщений.
Перед тем как начать общение Вам понадобиться псевдоним, под которым вы будете общаться.
Чтобы задать псевдоним воспользуйтесь командой '/NewName псевдоним'.
Чтобы отправлять сообщения Вам нужно ввести '/send username или псевдоним',
после вам нужно будет написать сообщение которое вы хотите отправить"""
    if reqv.chat.username == "mrsnowcats_kote":
        message = """Ну привет, Влад. Хуй тебе, а не инфа."""
    bot.send_message(reqv.chat.id, message)

@bot.message_handler(commands=["NewName"])
def NewName(reqv):
    name: str = reqv.text[7:].strip()
    if not check(name):
        pass
    else:
        bot.send_message(reqv.chat.id, """Такой псевдоним уже существует, введите команду вновь с другим именем""")

@bot.message_handler(commands=["send"])
def send(reqv):
    global CommandOfId
    name = reqv.text[6:]
    if check(name):
        if check(reqv.chat.username):
            bot.send_message(reqv.chat.id, """Напишите сообщение, которое хотите отправить""")
            CommandOfId.update({reqv.chat.id: [cmd.send, f"{name}"]})
        else:
            bot.send_message(reqv.chat.id,"""Перед тем как пользаваться ботом придумайте себе псевдоним командой '/NewName псевдоним'.""")    
    else:
        bot.send_message(reqv.chat.id, """Данный пользователь не зарегистрирован в боте. Проверьте правильность набора имени пользователя.""")

@bot.message_handler(content_types=["text"])
def handler_message(reqv):
    if reqv.chat.id in CommandOfId.keys():
        CommandOfId[reqv.chat.id][0](reqv)

if __name__ == "__main__":
    bot.polling(non_stop=True, interval=0)
    client.close()
    print("The bot has completed its work")
