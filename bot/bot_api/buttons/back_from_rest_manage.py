from bot.bot_api.buttons.buttons_settings.buttons_text import TEXT
from bot.bot_api.buttons.buttons_settings.callback_names import CallbackNames
from telegram import InlineKeyboardButton

back_from_rest_main: InlineKeyboardButton = InlineKeyboardButton(text=TEXT.back,
                                                                 callback_data=CallbackNames.back_from_rest_man)