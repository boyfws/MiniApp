from telegram import Bot

from bot.bot_api.keyboards.start_keyboard import start_keyboard
from bot.bot_api.config.message_text import TEXT_FOR_MESSAGES


async def send_start_message(chat_id: int, bot: Bot) -> None:
    await bot.send_message(chat_id=chat_id, text=TEXT_FOR_MESSAGES.start, reply_markup=start_keyboard)

