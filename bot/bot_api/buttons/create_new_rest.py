from bot.bot_api.buttons_text import TEXT_FOR_BUTTONS
from bot.bot_api.callback_names import CallbackNames
from telegram import InlineKeyboardButton


create_new_rest = InlineKeyboardButton(text=TEXT_FOR_BUTTONS.create_new_rest,
                                       callback_data=CallbackNames.create_new_rest)