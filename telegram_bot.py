from environs import Env

from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters

from dialogflow_respond_peocess import detect_intent_texts
import logging
from log_configuration import TGBotLogHandler

import google.api_core.exceptions


log = logging.getLogger(__file__)


def start(update, context):
    user = update.effective_user
    update.message.reply_text(
        f'Здравствуйте, {user["username"]}'
    )


def help_command(update, context):
    update.message.reply_text('Этот бот отвечает на ваши вопросы')


def bot_respond(update, context):
    try:
        respond = detect_intent_texts(
            project_id,
            update.message.chat.id,
            update.message.text,
            language_code
        )
        if respond:
            update.message.reply_text(respond.fulfillment_text)
    except google.api_core.exceptions.ServiceUnavailable:
        log.debug("DialogFlow недоступен")


def run_bot(token):
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, bot_respond)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':

    env = Env()
    env.read_env()

    token = env('TELEGRAM_TOKEN')
    project_id = env('PROJECT_ID')
    language_code = env('LANGUAGE_CODE')

    handler = TGBotLogHandler(env('CHAT_ID'), token)
    handler.setLevel(logging.DEBUG)
    log.addHandler(handler)
    log.info('Бот TG запущен')

    run_bot(token)
