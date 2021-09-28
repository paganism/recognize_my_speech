from environs import Env
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_respond_peocess import detect_intent_texts


def bot_respond(event, vk_api):
    respond = detect_intent_texts(
        project_id, event.user_id, event.text, language_code
    )
    if respond.intent.is_fallback:
        return
    vk_api.messages.send(
        user_id=event.user_id,
        message=respond.fulfillment_text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":

    env = Env()
    env.read_env()

    token = env('VK_TOKEN')
    language_code = env('LANGUAGE_CODE')
    project_id = env('PROJECT_ID')

    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            bot_respond(event, vk_api)
