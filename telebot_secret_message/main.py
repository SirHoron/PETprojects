from telebot import TeleBot
from cache import cache

bot = TeleBot("8403549969:AAGRdJvDRD5C8slSlMD2uzTaSwntu3MgHJw")

CommandOfId: dict[list] = {}

class Commands:
    def send(self, reqv):
        message = f"""*Тебе анонимно написали:*
    {reqv.text}"""
        bot.send_message(cache.get(CommandOfId[reqv.chat.id][1]), message, parse_mode="Markdown")
        CommandOfId.pop(reqv.chat.id)
cmd = Commands()


@bot.message_handler(commands=["start"])
def start(reqv):
    bot.send_message(reqv.chat.id,
"""Приветствую Вас, я тестовый бот.
Я буду выполнять различные задачи, и для того чтобы узнать
какую мне дали задачу ныне, введите /help.""")

@bot.message_handler(commands=["help"])
def help(reqv):
    message = """
Данный бот предназначен для анонимной отправки сообщений.
Чтобы отправить сообщение Вам нужно ввести '/send username или псевдоним',
после вам нужно будет написать сообщение которое вы хотите отправить"""
    if reqv.chat.username == "mrsnowcats_kote":
        message = """Ну привет, Влад. Хуй тебе, а не инфа."""
    bot.send_message(reqv.chat.id, message)

@bot.message_handler(commands=["send"])
def send(reqv):
    global CommandOfId
    name = reqv.text[6:]
    if cache.check(name):
        bot.send_message(reqv.chat.id, """Напишите сообщение, которое хотите отправить""")
        CommandOfId.update({reqv.chat.id: [cmd.send, f"{name}"]})
    else:
        bot.send_message(reqv.chat.id, """Данный пользователь не зарегистрирован в боте. Проверьте правильность набора имени пользователя.""")

@bot.message_handler(content_types=["text"])
def handler_message(reqv):
    try:
        CommandOfId[reqv.chat.id][0](reqv)
    except KeyError:
        pass

bot.polling(non_stop=True, interval=0)
