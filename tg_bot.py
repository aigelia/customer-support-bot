import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from environs import Env
from dialogflow_client import detect_intent_text
import traceback


async def command_start_handler(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Чем могу помочь?")


async def reply_handler(message: Message, bot: Bot, admin_chat_id: int):
    try:
        text, _ = await asyncio.to_thread(detect_intent_text, message.text, message.from_user.id)
        if text:
            await message.answer(text)
    except Exception as e:
        error_text = f"Ошибка в обработке сообщения от {message.from_user.id}:\n{e}\n{traceback.format_exc()}"
        await bot.send_message(admin_chat_id, error_text)


async def run_tg_bot():
    env = Env()
    env.read_env()
    tg_token = env.str("TG_TOKEN")
    admin_chat_id = env.int("ADMIN_CHAT_ID")

    bot = Bot(token=tg_token)
    dp = Dispatcher()

    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(lambda msg: reply_handler(msg, bot, admin_chat_id))

    try:
        await dp.start_polling(bot)
    except Exception as e:
        error_text = f"CRITICAL ERROR: {e}\n{traceback.format_exc()}"
        await bot.send_message(admin_chat_id, error_text)


if __name__ == "__main__":
    asyncio.run(run_tg_bot())
