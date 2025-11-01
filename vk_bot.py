import random
from environs import Env
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow_client import detect_intent_text


def send_vk_message(vk_api, user_id, text):
    vk_api.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1, 10000)
    )


def run_vk_bot():
    env = Env()
    env.read_env()
    vk_token = env.str("VK_TOKEN")

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api_obj = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type != VkEventType.MESSAGE_NEW or not event.to_me:
            continue

        user_text = event.text
        user_id = event.user_id

        df_response, is_fallback = detect_intent_text(user_text, user_id)
        if not is_fallback and df_response:
            send_vk_message(vk_api_obj, user_id, df_response)


if __name__ == "__main__":
    run_vk_bot()
