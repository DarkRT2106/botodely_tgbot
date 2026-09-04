import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ==============================
# НАСТРОЙКИ
# ==============================

TOKEN = os.getenv("8998464096:AAEOiTAZurW53o1RCAx5hO_gG8AjxWeUslQ")

MANAGER_USERNAME = "@RT_ATC1026"


if not TOKEN:
    raise ValueError("Переменная BOT_TOKEN не установлена!")


# ==============================
# БОТ
# ==============================

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ==============================
# /start
# ==============================

@dp.message(CommandStart())
async def start(message: types.Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⏱ Сколько делается бот?",
                    callback_data="time"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 Сколько стоит бот?",
                    callback_data="price"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📞 Написать менеджеру",
                    callback_data="manager"
                )
            ]
        ]
    )

    await message.answer(
        "Здравствуйте! 👋\n\n"
        "Если вы хотите заказать Telegram-бота для своего бизнеса и не только, "
        "вы можете выбрать один из вариантов ниже:",
        reply_markup=keyboard
    )


# ==============================
# ОБРАБОТКА КНОПОК
# ==============================

@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):

    if callback.data == "time":

        await callback.message.answer(
            "⏱ Точное время назвать нельзя — "
            "всё зависит от сложности и функционала бота."
        )

    elif callback.data == "price":

        await callback.message.answer(
            "💰 Стоимость разработки бота — "
            "от 500 ₽ за самого простого бота "
            "до 2000 ₽ и выше, в зависимости от сложности."
        )

    elif callback.data == "manager":

        await callback.message.answer(
            f"📞 Если вы хотите обсудить создание бота, "
            f"менеджеру можно написать в личные сообщения:\n\n"
            f"{MANAGER_USERNAME}"
        )

    await callback.answer()


# ==============================
# ЗАПУСК
# ==============================

async def main():

    print("Бот запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())