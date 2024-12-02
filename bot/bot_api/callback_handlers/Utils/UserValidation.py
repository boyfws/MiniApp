from bot_api.bot_utils import injection_notifier_logger
from bot_api.external_api import check_user_roots

from .Logger import Logger


class UserValidation(Logger):
    def __init__(self):
        pass

    async def validate_user(self, rest_id: int, user_id: int) -> bool:
        """
        Обертка для check user roots с логгированием, возвращает False если пользователю отказано
        возвращает True, если пользователю можно работать с рестораном False иначе
        """
        if not await check_user_roots(rest_id=rest_id, user_id=user_id):
            self._log_roots_validation_error(user_id=user_id, rest_id=rest_id)
            return False
        return True