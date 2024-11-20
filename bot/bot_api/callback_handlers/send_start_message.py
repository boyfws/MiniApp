from telegram import Bot

from bot.bot_api.keyboards.keyboards import start_keyboard
from bot.bot_api.config.message_text import TEXT_FOR_MESSAGES

from typing import Optional

from bot.bot_api.bot_utils.logger import user_activity_logger


async def send_start_message(chat_id: int,
                             bot: Bot,
                             log: Optional[bool] = False) -> None:
    await bot.send_message(chat_id=chat_id, text=TEXT_FOR_MESSAGES.start, reply_markup=start_keyboard)
    if log:
        user_activity_logger.info(f"Пользователь вернулся на главную страницу")
