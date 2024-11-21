from telegram.ext import MessageHandler, ConversationHandler, ContextTypes

from telegram import Update

from bot_api.config import *

from bot_api.bot_handlers import (start_command,
                                  add_rest_conv_callback_query as callback_query)


add_rest_conv_handler = ConversationHandler(
    entry_points=[callback_query],
    states={
        INHERITANCE: [callback_query],
        NAME: []
    },
    fallbacks=[callback_query, start_command],
)
