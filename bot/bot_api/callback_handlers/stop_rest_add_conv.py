from bot.bot_api.config.message_text import TEXT_FOR_MESSAGES
from telegram.ext import ConversationHandler

from bot.bot_api.bot_utils.logger import user_activity_logger


async def stop_rest_add_conv(user_id: int) -> None:
    user_activity_logger.info(f"Пользователь {user_id} досрочно завершил добавление ресторана")
