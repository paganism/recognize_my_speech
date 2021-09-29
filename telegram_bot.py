from environs import Env

from telegram import Update
from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, CallbackContext

from dialogflow_respond_peocess import detect_intent_texts
import logging
from log_configuration import TGBotLogHandler

import google.api_core.exceptions


log = logging.getLogger(__file__)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(
        f'Здравствуйте, {user["username"]}'
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Этот бот отвечает на ваши вопросы')


def bot_respond(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    try:
        respond = detect_intent_texts(
            project_id, update.message.chat.id, update.message.text, language_code
        )
    except google.api_core.exceptions.ServiceUnavailable:
        log.debug("DialogFlow недоступен")

    except Exception as ex:
        log.debug(ex)
    update.message.reply_text(respond.fulfillment_text)


if __name__ == '__main__':

    env = Env()
    env.read_env()

    token = env('TELEGRAM_TOKEN')
    session_id = env('CHAT_ID')
    project_id = env('PROJECT_ID')
    language_code = env('LANGUAGE_CODE')

    updater = Updater(token)
    
    dispatcher = updater.dispatcher

    handler = TGBotLogHandler(session_id, token)
    handler.setLevel(logging.DEBUG)
    log.addHandler(handler)

    log.info('Бот запущен')

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, bot_respond)
    )

    updater.start_polling()
    updater.idle()
