import asyncio

import httpx
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from environs import Env



async def command_start_handler(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")


async def echo_handler(message: Message):
    await message.send_copy(chat_id=message.chat.id)


async def main():
    env = Env()
    env.read_env()
    tg_token = env.str("TG_TOKEN")

    bot = Bot(token=tg_token)
    dp = Dispatcher()

    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(echo_handler)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
