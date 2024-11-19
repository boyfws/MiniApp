from bot.bot_api.config.buttons_text import TEXT_FOR_BUTTONS
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def back_to_this_message_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [

            [
                InlineKeyboardButton(text=TEXT_FOR_BUTTONS.back_to_message,
                                     callback_data=callback_data)
            ]
        ]
    )
