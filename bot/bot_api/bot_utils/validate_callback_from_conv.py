from .mypy_types import Update_mod, CallbackQuery_mod
from .logger import injection_notifier_logger


def val_callback_from_conv(query: CallbackQuery_mod, update: Update_mod) -> str | None:
    """
    Проверяет callback из Conversation на правильность, возвращает
    колбэк без префикса если все в порядке None иначе
    """
    user_id = update.effective_user.id

    try:
        callback = query.data.split("_")[1]
        return callback
    except ValueError:
        injection_notifier_logger.warning(f"Пользователь {user_id} отправил callback с более чем одним символом '_'")
        return None