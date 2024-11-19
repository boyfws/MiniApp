from telegram.ext import MessageHandler, ConversationHandler, ContextTypes
from telegram import Update
from bot.bot_api.bot_handlers.create_new_rest import create_new_rest_start_point
from bot.bot_api.bot_handlers.stop_conversation import stop_conversation
from bot.bot_api.config.state_names_for_adding_rest import *


add_rest_conv = ConversationHandler(
    entry_points=[create_new_rest_start_point],
    states={},
    fallbacks=[stop_conversation]
)
