from bot.bot_api.buttons.create_new_rest import create_new_rest
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Tuple

from bot.bot_api.bot_config import MAX_INLINE_BUTTON_LEN

from bot.bot_api.bot_utils.truncate_text import truncate_text

from bot.bot_api.callback_names import CallbackNames


def get_rest_man_keyboard(rest_data: List[
    Tuple[str, int]
]) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для сообщения с управлением и добавлением ресторанов
    Данные передаются в формате [(name: str, id: int)...]
    """
    rest_buttons = [
        [
            InlineKeyboardButton(text=truncate_text(el[0], MAX_INLINE_BUTTON_LEN),
                                 callback_data=f"{CallbackNames.show_rest_info}:{el[1]}")
        ]
        for el in rest_data
    ]
    return InlineKeyboardMarkup(
         rest_buttons + [[create_new_rest]]
    )
