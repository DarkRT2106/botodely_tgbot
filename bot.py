import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ==============================
# НАСТРОЙКИ
# ==============================

TOKEN = os.getenv("BOT_TOKEN")

# СЮДА ПОТОМ ВСТАВИМ ТВОЙ TELEGRAM ID
MANAGER_ID = 7260290486


if not TOKEN:
    raise ValueError("Переменная BOT_TOKEN не установлена!")


bot = Bot(token=TOKEN)
dp = Dispatcher()


# ==============================
# КЛАВИАТУРА
# ==============================

def main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Написать менеджеру",
                    callback_data="manager"
                )
            ]
        ]
    )


# ==============================
# /START
# ==============================

@dp.message(CommandStart())
async def start(message: types.Message):

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
        reply_markup=main_keyboard()
    )


# ==============================
# КНОПКА "НАПИСАТЬ МЕНЕДЖЕРУ"
# ==============================

@dp.callback_query(lambda callback: callback.data == "manager")
async def manager_button(callback: types.CallbackQuery):

    await callback.message.answer(
        "💬 Здесь Вы можете написать сообщение менеджеру.\n\n"
        "Просто отправьте следующим сообщением свой вопрос или сообщение, "
        "и мы передадим его менеджеру."
    )

    await callback.answer()


# ==============================
# ПОЛУЧЕНИЕ СООБЩЕНИЙ
# ==============================

@dp.message()
async def receive_message(message: types.Message):

    # Не обрабатываем команды
    if message.text and message.text.startswith("/"):
        return

    user = message.from_user

    username = f"@{user.username}" if user.username else "нет username"

    # Информация о клиенте
    user_info = (
        "📩 НОВОЕ СООБЩЕНИЕ ОТ КЛИЕНТА\n\n"
        f"👤 Имя: {user.full_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 Telegram ID: {user.id}\n\n"
        "💬 Сообщение:\n"
    )

    # Если пользователь отправил текст
    if message.text:
        await bot.send_message(
            MANAGER_ID,
            user_info + message.text
        )

    # Если отправил фото
    elif message.photo:
        await bot.send_message(
            MANAGER_ID,
            user_info + "Клиент отправил фотографию:"
        )

        await bot.send_photo(
            MANAGER_ID,
            message.photo[-1].file_id,
            caption=message.caption or ""
        )

    # Если отправил видео
    elif message.video:
        await bot.send_message(
            MANAGER_ID,
            user_info + "Клиент отправил видео:"
        )

        await bot.send_video(
            MANAGER_ID,
            message.video.file_id,
            caption=message.caption or ""
        )

    # Остальные типы сообщений
    else:
        await bot.send_message(
            MANAGER_ID,
            user_info + "Клиент отправил сообщение, которое бот пока не умеет пересылать."
        )

    # Ответ клиенту
    await message.answer(
        "✅ Сообщение отправлено менеджеру!\n\n"
        "Обязательно отключите платное отправление сообщений и т.д. что бы менеджер мог вам написать!. "
        "Менеджер свяжется с Вами в ближайшее время.",
        reply_markup=main_keyboard()
    )


# ==============================
# ЗАПУСК
# ==============================

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

