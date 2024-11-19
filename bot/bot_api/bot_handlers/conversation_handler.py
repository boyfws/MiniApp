from telegram.ext import MessageHandler, ConversationHandler, ContextTypes
from telegram import Update

from bot.bot_api.config.state_names_for_adding_rest import *

from bot.bot_api.bot_handlers.start_command import start_command
from bot.bot_api.bot_handlers.conversation_add_rest_callback_query import conversation_add_rest_callback_query as callback_query


async def perm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("ASASASASa")
    context.bot.send_message(chat_id=update.effective_chat.id, text="dada")


add_rest_conv = ConversationHandler(
    entry_points=[callback_query],
    states={
        INHERITANCE: [MessageHandler(callback=perm, filters=None), callback_query],
        NAME: [MessageHandler(callback=perm, filters=None)]
    },
    fallbacks=[callback_query, start_command],
    per_message=True
)
