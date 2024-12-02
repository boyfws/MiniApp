from bot_api.bot_utils import user_activity_logger, injection_notifier_logger
from typing import Any


class Logger:
    @staticmethod
    def _log_create_new_rest(user_id: int, flag: bool) -> None:
        if not flag:
            user_activity_logger.info(f"Пользователь {user_id} вернулся к стартовой странице для наследования")
        else:
            user_activity_logger.info(f"Пользователь {user_id} начал создание ресторана")

    @staticmethod
    def _log_handle_rest_click(user_id: int, rest_id: int, flag: bool) -> None:
        if flag:
            user_activity_logger.info(f"Пользователь {user_id} перешел на страницу ресторана {rest_id}")
        else:
            user_activity_logger.info(f"Пользователь {user_id} вернулся на страницу ресторана")

    @staticmethod
    def _log_switch_to_rest_management(flag: bool, user_id: int) -> None:
        if flag:
            user_activity_logger.info(f"Пользователь {user_id} перешел на страницу управления ресторанами")
        else:
            user_activity_logger.info(f"Пользователь {user_id} вернулся на старицу управления ресторанами")

    @staticmethod
    def _log_move_on_from_inheritance(user_id: int) -> None:
        user_activity_logger.info(f"Пользователь {user_id} закончил наследование свойств своих ресторанов")

    @staticmethod
    def _log_arg_validation_error(user_id: int, arg: Any, dtype: type) -> None:
        injection_notifier_logger.warning(
            f"От пользователя {user_id} поступил callback с аргументами непрошедшими валидацию: {arg}. Ожидаемый тип: {dtype}"
        )

    @staticmethod
    def _log_roots_validation_error(user_id: int, rest_id: int) -> None:
        injection_notifier_logger.error(
            f"Пользователь {user_id} попытался получить доступ не к своему ресторану {rest_id}"
        )

    @staticmethod
    def _log_stop_rest_add_conv(user_id: int):
        user_activity_logger.info(f"Пользователь {user_id} досрочно завершил добавление ресторана")

