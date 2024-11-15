from telegram import InlineKeyboardButton
from bot.bot_api.buttons_text import TEXT_FOR_BUTTONS
from bot.bot_api.callback_names import CallbackNames

switch_to_rest_management: InlineKeyboardButton = InlineKeyboardButton(text=TEXT_FOR_BUTTONS.switch_to_rest_management,
                                                                       callback_data=CallbackNames.switch_to_rest_management)