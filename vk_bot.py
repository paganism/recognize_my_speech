from environs import Env
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_respond_peocess import detect_intent_texts
from log_configuration import TGBotLogHandler
import google.api_core.exceptions
import logging


log = logging.getLogger(__file__)


def get_dataflow_respond(event, vk_api):
    user = f'vk-{event.user_id}'
    respond = detect_intent_texts(
        project_id, user, event.text, language_code
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

    tg_bot_token = env("TELEGRAM_TOKEN")
    log_chat_id = env("CHAT_ID")

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    log.setLevel(logging.DEBUG)
    log.addHandler(TGBotLogHandler(log_chat_id, tg_bot_token))
    log.info('Бот vk запущен')

    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                get_dataflow_respond(event, vk_api)
            except google.api_core.exceptions.ServiceUnavailable:
                log.info("DialogFlow недоступен")
