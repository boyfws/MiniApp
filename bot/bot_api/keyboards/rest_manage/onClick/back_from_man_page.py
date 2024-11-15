from telegram import Update
from telegram.ext import CallbackContext


async def back_from_man_page(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    chat_id = query.message.chat_id
    message_id = query.message.message_id
    await context.bot.delete_message(chat_id=chat_id,
                                     message_id=message_id)
