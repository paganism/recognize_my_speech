import logging
import telegram


class TGBotLogHandler(logging.Handler):

    def __init__(self, chat_id, tg_token):
        super().__init__()
        self.chat_id = chat_id
        self.tg_token = tg_token
        self.bot = telegram.Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(text=log_entry, chat_id=self.chat_id)
