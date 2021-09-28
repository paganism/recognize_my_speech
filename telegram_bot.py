from environs import Env

from telegram import Update
from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, CallbackContext

from dialogflow_respond_peocess import detect_intent_texts


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(
        f'Здравствуйте, {user["username"]}'
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def bot_respond(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    respond = detect_intent_texts(
        project_id, update.message.chat.id, update.message.text, language_code
    )
    update.message.reply_text(respond.fulfillment_text)


if __name__ == '__main__':

    env = Env()
    env.read_env()

    token = env('TELEGRAM_TOKEN')
    session_id = env('CHAT_ID')
    project_id = env('PROJECT_ID')
    language_code = env('LANGUAGE_CODE')

    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - bot respond the message on Telegram
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, bot_respond)
    )
    # Start the Bot
    updater.start_polling()
    updater.idle()
