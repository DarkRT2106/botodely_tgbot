import asyncio
import os
import threading

from flask import Flask

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ==============================
# НАСТРОЙКИ
# ==============================

TOKEN = os.getenv("BOT_TOKEN")

MANAGER_USERNAME = "@RT_ATC1026"

PORT = int(os.getenv("PORT", 10000))


if not TOKEN:
    raise ValueError("Переменная BOT_TOKEN не установлена!")


# ==============================
# HTTP-СЕРВЕР ДЛЯ RENDER
# ==============================

app = Flask(__name__)


@app.route("/")
def home():
    return "Bot is running!"


def run_web_server():
    app.run(
        host="0.0.0.0",
        port=PORT
    )


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
                    text="📞 Написать менеджеру",
                    callback_data="manager"
                )
            ]
        ]
    )

    await message.answer(
        "Вас приветствует мини-студия Ботоделы! 👋\n\n"
        "Каждого бота мы делаем качественно! 🔥",
        "Поэтому создание каждого бота занимает около полутора недель",
        "Все зависит от количества работы 😉",
        "Цена колеблится от 500₽ до 2000₽",
        "Если вы хотите задать вопрос или заказать Telegram-бота для своего бизнеса и не только, "
        "вы можете выбрать один из вариантов ниже:",
        reply_markup=keyboard
    )


# ==============================
# ОБРАБОТКА КНОПОК
# ==============================

@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):


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

    # Запускаем HTTP-сервер в отдельном потоке
    web_thread = threading.Thread(
        target=run_web_server,
        daemon=True
    )

    web_thread.start()

    # Запускаем Telegram-бота
    asyncio.run(main())
