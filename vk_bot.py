import os
import random

from environs import Env
from google.cloud import dialogflow_v2 as dialogflow
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

env = Env()
env.read_env()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env.str("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = env.str("PROJECT_ID")
VK_TOKEN = env.str("VK_TOKEN")


def get_dialogflow_response(text, user_id):
    client = dialogflow.SessionsClient()
    session = client.session_path(PROJECT_ID, str(user_id))

    text_input = dialogflow.TextInput(text=text, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)

    response = client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text


def send_vk_message(vk_api, user_id, text):
    vk_api.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk_api_obj = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_text = event.text
            user_id = event.user_id

            print(f"Сообщение от {user_id}: {user_text}")

            df_response = get_dialogflow_response(user_text, user_id)
            send_vk_message(vk_api_obj, user_id, df_response)
