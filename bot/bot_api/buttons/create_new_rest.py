from bot.bot_api.buttons.buttons_settings.buttons_text import TEXT
from bot.bot_api.buttons.buttons_settings.callback_names import CallbackNames
from telegram import InlineKeyboardButton


create_new_rest = InlineKeyboardButton(text=TEXT.create_new_rest,
                                       callback_data=CallbackNames.create_new_rest)