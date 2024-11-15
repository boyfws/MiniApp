from telegram import Update
from telegram.ext import CallbackContext

from bot.bot_api.message_text import TEXT_FOR_MESSAGES


async def show_rest_info(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    # Выполняются запросы к БД

    text = TEXT_FOR_MESSAGES.get_text_for_rest_mes("Eboba", "Москва", "Патриарши пруды", "8")
    await context.bot.send_message(chat_id=chat_id, text=text)
