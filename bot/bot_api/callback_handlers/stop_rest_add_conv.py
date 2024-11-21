from bot_api.config import TextForMessages

from bot_api.bot_utils import user_activity_logger


async def stop_rest_add_conv(user_id: int) -> None:
    user_activity_logger.info(f"Пользователь {user_id} досрочно завершил добавление ресторана")
