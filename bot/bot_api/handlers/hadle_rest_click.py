from telegram.ext import CallbackQueryHandler
from telegram import Update
from telegram.ext import CallbackContext


async def handle_rest_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()


rest_click: CallbackQueryHandler = CallbackQueryHandler(handle_rest_click, pattern=r'^\d+$')
# Обрабатываем толко числа, выделены для номеров ресторанов
