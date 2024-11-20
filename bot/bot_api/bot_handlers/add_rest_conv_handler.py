from telegram.ext import MessageHandler, ConversationHandler, ContextTypes
from telegram import Update

from bot.bot_api.config.state_names_for_rest_add_conv import *

from bot.bot_api.bot_handlers.start_command import start_command
from bot.bot_api.bot_handlers.add_rest_conv_callback_query import add_rest_conv_callback_query as callback_query


add_rest_conv_handler = ConversationHandler(
    entry_points=[callback_query],
    states={
        INHERITANCE: [callback_query],
        NAME: []
    },
    fallbacks=[callback_query, start_command],
)
