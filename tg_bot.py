import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from environs import Env
from dialogflow_client import detect_intent_text


async def command_start_handler(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Чем могу помочь?")


async def reply_handler(message: Message):
    text, _ = await asyncio.to_thread(detect_intent_text, message.text, message.from_user.id)
    if text:
        await message.answer(text)


async def run_tg_bot():
    env = Env()
    env.read_env()
    tg_token = env.str("TG_TOKEN")

    bot = Bot(token=tg_token)
    dp = Dispatcher()

    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(reply_handler)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_tg_bot())
