from telegram import Update
from telegram.ext import CallbackContext

from bot.bot_api.keyboards.start_keyboard import start_keyboard
from bot.bot_api.message_text import TEXT_FOR_MESSAGES


async def send_start_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=TEXT_FOR_MESSAGES.start, reply_markup=start_keyboard)

