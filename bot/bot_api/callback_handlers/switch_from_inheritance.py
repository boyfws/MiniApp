from bot.bot_api.bot_utils.logger import user_activity_logger


async def switch_from_inheritance(user_id: int) -> None:
    user_activity_logger.info(f"Пользователь {user_id} закончил наследование свойств своих ресторанов")
