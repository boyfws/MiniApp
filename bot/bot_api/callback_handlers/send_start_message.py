from telegram import Bot

from bot_api.keyboards import start_keyboard
from bot_api.config import TextForMessages

from typing import Optional

from bot_api.bot_utils import user_activity_logger


async def send_start_message(chat_id: int,
                             bot: Bot,
                             log: Optional[bool] = False) -> None:
    await bot.send_message(chat_id=chat_id, text=TextForMessages.start, reply_markup=start_keyboard)
    if log:
        user_activity_logger.info(f"Пользователь вернулся на главную страницу")
