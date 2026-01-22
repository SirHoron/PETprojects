from telebot.async_telebot import AsyncTeleBot
import asyncio
from clientpack.asuncreqv import *

bot = AsyncTeleBot("8403549969:AAGRdJvDRD5C8slSlMD2uzTaSwntu3MgHJw")

CommandOfId: dict[list] = {}
class Commands:
    async def send(self, reqv):
        print(reqv.text)
        message = f"""*Тебе анонимно написали:*
    {reqv.text}"""
        data = await asyncio.create_task(get(CommandOfId[reqv.chat.id][1]))
        if data:
            await asyncio.create_task(bot.send_message(data[2], message, parse_mode="Markdown"))
            CommandOfId.pop(reqv.chat.id)
        else:
            print("[ошибка] некорректная data в cmd.send")
cmd = Commands()

@bot.message_handler(commands=["start"])
async def start(reqv):
    global answer
    print("gfv")
    await asyncio.create_task(bot.send_message(reqv.chat.id,
"""Приветствую Вас, я тестовый бот.
Я буду выполнять различные задачи, и для того чтобы узнать
какую мне дали задачу ныне, введите /help."""))

@bot.message_handler(commands=["help"])
async def help(reqv):
    global answer
    message = """
Данный бот предназначен для анонимной отправки сообщений.
Перед тем как начать общение Вам понадобиться псевдоним, под которым вы будете общаться.
Чтобы задать псевдоним воспользуйтесь командой '/NewName псевдоним'.
Чтобы отправлять сообщения Вам нужно ввести '/send username или псевдоним',
после вам нужно будет написать сообщение которое вы хотите отправить"""
    if reqv.chat.username == "mrsnowcats_kote":
        message = """Ну привет, Влад. Хуй тебе, а не инфа."""
    await asyncio.create_task(bot.send_message(reqv.chat.id, message))

@bot.message_handler(commands=["NewName"])
async def NewName(reqv):
    global answer
    name: str = reqv.text.split(" ")[1].strip()
    if not await asyncio.create_task(check(name)):
        if not await asyncio.create_task(check(reqv.chat.username)):
            if await asyncio.create_task(new(reqv.chat.username, name, reqv.chat.id)):
                await asyncio.create_task(bot.send_message(reqv.chat.id, """Поздавляю теперь вы можете писать другим людям через команду '/send username или псевдоним'"""))
        else:
            await asyncio.create_task(bot.send_message(reqv.chat.id, """У Вас уже есть псевдоним чтобы его переназначить воспользуйтесь командой '/ResetName псевдоним'"""))
    else:
        await asyncio.create_task(bot.send_message(reqv.chat.id, """Такой псевдоним уже существует, введите команду вновь с другим именем"""))

@bot.message_handler(commands=["ResetName"])
async def ResetName(reqv):
    global answer
    name: str = reqv.text.split(" ")[1].strip()
    if not await asyncio.create_task(check(name)):
        if await asyncio.create_task(check(reqv.chat.username)):
            if await asyncio.create_task(update(name, reqv.chat.id)):
                await asyncio.create_task(bot.send_message(reqv.chat.id, f"""Поздравляю теперь Вас зовут {name} """))
        else:
            await asyncio.create_task(bot.send_message(reqv.chat.id, """У вас ещё не задан псевдоним, воспользуйтесь командой '/NewName псевдоним'"""))
    else:
        await asyncio.create_task(bot.send_message(reqv.chat.id, """Такой псевдоним уже существует, введите команду вновь с другим именем"""))


@bot.message_handler(commands=["send"])
async def send(reqv):
    global answer
    global CommandOfId
    name = reqv.text.split(" ")
    name = name[len(name)-1]
    if await asyncio.create_task(check(name)):
        if await asyncio.create_task(check(reqv.chat.username)):
            await asyncio.create_task(bot.send_message(reqv.chat.id, """Напишите сообщение, которое хотите отправить"""))
            CommandOfId.update({reqv.chat.id: [cmd.send, f"{name}"]})
        else:
            await asyncio.create_task(bot.send_message(reqv.chat.id, """Прежде чем писать другим пользователям, задайте псевдоним командой '/NewName имя'"""))
    else:
        await asyncio.create_task(bot.send_message(reqv.chat.id, """Данный пользователь не зарегистрирован в боте. Проверьте правильность набора имени пользователя."""))

@bot.message_handler(content_types=["text"])
async def handler_message(reqv):
    global answer
    if reqv.chat.id in CommandOfId.keys():
        await asyncio.create_task(CommandOfId[reqv.chat.id][0](reqv))


def main():
    print("Bot start")
    asyncio.run(bot.polling(non_stop=True, interval=0))
    print("The bot has completed its work")

if  flage_1:
    main()
