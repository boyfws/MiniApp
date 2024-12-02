from telegram.ext import ConversationHandler

from bot_api.config import *

from .start_command import start_command
from .add_rest_conv_callback_query import add_rest_conversation_callback_query as callback_query


add_rest_conv_handler = ConversationHandler(
    entry_points=[callback_query],
    states={
        INHERITANCE: [callback_query],
        NAME: []
    },
    fallbacks=[callback_query, start_command],
)
