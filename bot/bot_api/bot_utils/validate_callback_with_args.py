from .logger import injection_notifier_logger
from telegram import CallbackQuery, Update

from typing import Tuple

from .validate_callback_from_conv import val_callback_from_conv


def val_callback_with_args(query: CallbackQuery, update: Update) -> Tuple[str, str] | Tuple[None, None]:
    """
    Валидирует колбэк с аргументами, возвращает имя колбэка и
    аргумент если все в порядке None, None иначе
    """
    user_id = update.effective_user.id

    try:
        if "_" in query.data:
            callback_str = val_callback_from_conv(query=query, update=update)
        else:
            callback_str = query.data

        callback_name, arg = callback_str.split(":")
        return callback_name, arg
    except ValueError:
        injection_notifier_logger.warning(
            f"От пользователя {user_id} поступил callback с двумя символами ':': {query.data}")
        return None, None