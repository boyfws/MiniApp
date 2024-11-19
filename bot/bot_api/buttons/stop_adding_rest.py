from bot.bot_api.config.buttons_text import TEXT_FOR_BUTTONS
from bot.bot_api.config.callback_names import CallbackNames
from telegram import InlineKeyboardButton

stop_adding_rest = InlineKeyboardButton(text=TEXT_FOR_BUTTONS.stop_rest_adding,
                                        callback_data=CallbackNames.stop_rest_adding)
