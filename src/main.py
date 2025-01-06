import asyncio
import logging
import sys
import os
import db
# from watchfiles import awatch
from dotenv import load_dotenv

load_dotenv()

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.environ.get("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

instruction = ""
with open("README.md", "r") as instruction_file:
    pass_lines = True

    for line in instruction_file.readlines():
        parsed_line = line

        if "Как пользоваться" in parsed_line:
            pass_lines = False
        elif not pass_lines:
            instruction += parsed_line
    

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    # await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await message.answer(instruction)


@dp.message(Command("write"))
async def command_write_handler(message: Message, command: CommandObject) -> None:
    if command.args is None or len(command.args.split()) > 1:
        await message.answer("Укажите одно слово после команды")
        return
    
    parsed_word = command.args.strip().lower()

    try:
        translate = await db.write_word(message.from_user.id, parsed_word)
    except Exception as error:
        await message.answer(f"Произошла ошибка {error}")
    else:
        await message.answer(f"Перевод - {translate}")


@dp.message(Command("show"))
async def command_show_handler(message: Message) -> None:
    from_db = sorted(db.show_words(message.from_user.id), key=lambda x: x[1], reverse=True)

    if len(from_db) == 0:
        await message.answer("Словарь пуст")
        return

    res = map(lambda x: f"{x[0]} - {x[1]}", from_db)
    await message.answer("\n".join(list(res)))


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     """
#     Handler will forward receive a message back to the sender

#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    db.initialize_db()
    asyncio.run(main())