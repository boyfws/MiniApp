from telegram import InlineKeyboardButton
from bot.bot_api.buttons.buttons_settings.buttons_text import TEXT
from bot.bot_api.buttons.buttons_settings.callback_names import CallbackNames

switch_to_rest_management: InlineKeyboardButton = InlineKeyboardButton(text=TEXT.switch_to_rest_management,
                                                                callback_data=CallbackNames.switch_to_rest_management)