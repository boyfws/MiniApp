from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Tuple

from .buttons import *

from bot_api.bot_utils import truncate_text

from bot_api.config import (NamesForCallback,
                            TextForButtons,
                            MAX_INLINE_BUTTON_LEN)


def get_rest_management_keyboard(rest_data: List[
    Tuple[str, int]
]) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для сообщения с управлением и добавлением ресторанов
    Данные передаются в формате [(name: str, id: int)...]
    """
    rest_buttons = [
        [
            InlineKeyboardButton(text=truncate_text(el[0], MAX_INLINE_BUTTON_LEN),
                                 callback_data=f"{NamesForCallback.show_rest_info}:{el[1]}")
        ]
        for el in rest_data
    ]
    return InlineKeyboardMarkup(
        rest_buttons + [[create_new_rest]]
    )


def back_to_this_message_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [

            [
                InlineKeyboardButton(text=TextForButtons.back_to_message,
                                     callback_data=callback_data)
            ]
        ]
    )


start_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup([
    [link_to_miniapp],
    [switch_to_rest_management]
])

stop_rest_add_conv_keyb = InlineKeyboardMarkup([
    [
        stop_rest_conv_button
    ]
])


def rest_for_inheritance_keyboard(rest_data: List[
    Tuple[str, int]
]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text=truncate_text(el[0], MAX_INLINE_BUTTON_LEN),
                                  callback_data=f"{NamesForCallback.adding_rest_conv_mark}_{NamesForCallback.inheritance_property_of_rest}:{el[1]}")]
            for el in rest_data
        ] + [[stop_rest_conv_button], [switch_from_inheritance]]
    )


def inheritance_properties_keyboard(
        rest_id: int,
        properties: Tuple[str, ...]
) -> InlineKeyboardMarkup:
    rest_prop = [
        [
            InlineKeyboardButton(text=getattr(TextForButtons, el),
                                 callback_data=f"{NamesForCallback.adding_rest_conv_mark}_{getattr(NamesForCallback, el)}:{rest_id}")
        ]
        for el in properties
    ]
    return InlineKeyboardMarkup(rest_prop)
