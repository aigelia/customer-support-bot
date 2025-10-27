import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from environs import Env
from google.cloud import dialogflow_v2 as dialogflow

env = Env()
env.read_env()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env.str("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = env.str("PROJECT_ID")


def get_dialogflow_response(text, user_id):
    client = dialogflow.SessionsClient()
    session = client.session_path(PROJECT_ID, str(user_id))

    text_input = dialogflow.TextInput(text=text, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)

    response = client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text


async def command_start_handler(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Чем могу тебе помочь?")


async def reply_handler(message: Message):
    reply_text = await asyncio.to_thread(
        get_dialogflow_response,
        message.text, message.from_user.id
    )
    await message.answer(reply_text or "Извини, я пока не знаю, что ответить.")


async def main():
    tg_token = env.str("TG_TOKEN")

    bot = Bot(token=tg_token)
    dp = Dispatcher()

    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(reply_handler)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
