import os, sys
from pprint import pprint

print(1)
pprint(sys.path)

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, BotCommand
import logging, time
import db_func

print(2)
pprint(sys.path)


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = "6677221607:AAHrLuwexT2MglaQTLtaEBg_N-70mn_PM2w"

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command="/help", description="Справка по работе бота"),
        BotCommand(command="/support", description="Поддержка"),
    ]

    await bot.set_my_commands(main_menu_commands)


async def process_support_command(message: Message):
    await message.answer("Отправте фото с сигаретой для того чтобы заблюирть сигарету")


# Этот хэндлер будет срабатывать на команду "/start"
async def process_start_command(message: Message):
    await message.answer(
        "Привет!\nМеня зовут Эхо-бот!\nЯ умею цензурить сигареты на фото.\nОтправь мне фотографию с сигаретой."
    )


# Этот хэндлер будет срабатывать на команду "/help"
async def process_help_command(message: Message):
    await message.answer("Отправте фото с сигаретой для того чтобы заблюирть сигарету")


# Этот хэндлер будет срабатывать на отправку боту фото
async def send_photo_echo(message: Message):
    await bot.download(message.photo[-1].file_id, "test.jpg")

    # ЗДЕСЬ САНЯ ВСТАВИТ Ф-ЦИЮ

    chat_id = message.from_user.id
    photo_path = FSInputFile("1.jpg")
    await bot.send_photo(chat_id, photo=photo_path)
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_message = message.text  # получаем текст сообщения
    logging.info(
        f"user_id={user_id}, user_full_name={user_full_name}, user_message={user_message}, time={time.asctime()}"
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
# async def send_echo(message: Message):
#     await message.reply(text=message.text)
# user_id = message.from_user.id
# user_full_name = message.from_user.full_name
# user_message = message.text  # получаем текст сообщения
# logging.info(
#     f"user_id={user_id}, user_full_name={user_full_name}, user_message={user_message}, time={time.asctime()}"
# )


# Регистрируем хэндлеры
dp.message.register(process_start_command, Command(commands="start"))
dp.message.register(process_help_command, Command(commands="help"))
dp.message.register(process_support_command, Command(commands="support"))
dp.message.register(send_photo_echo, F.photo)
# dp.message.register(send_echo)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
