import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = os.getenv("BOT_TOKEN")
MANAGER_USERNAME = "@botodel_manager"


if not TOKEN:
    raise ValueError("Переменная BOT_TOKEN не установлена")


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📞 Написать менеджеру",
                    url="https://t.me/RT_ATC1026"
                )
            ]
        ]
    )

    await message.answer(
        "Здравствуйте! 👋\n\n"
        "Мы Ботоделы, создаем телеграм ботов на ваш вкус, "
        "и подстраиваем его под ваши задачи.\n\n"
        "Каждого бота мы делаем качественно!\n"
        "Поэтому создание бота занимает около недели.\n\n"
        "Стоимость зависит от сложности бота.\n"
        "Это примерно от 500 до 2000 рублей.\n\n"
        "Для каждого бота нужен хостинг, а хороший хостинг стоит денег, "
        "поэтому хостинг для своего бота Вы оплачиваете САМИ!\n\n"
        "Об этом и не только Вы можете спросить менеджера "
        "по кнопке ниже ↓↓↓",
        reply_markup=keyboard
    )


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

