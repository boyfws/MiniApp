from telegram import InlineKeyboardMarkup

from ..buttons.link_to_miniapp_ru import link_to_miniapp_ru

start_keyboard_ru: InlineKeyboardMarkup = InlineKeyboardMarkup([
    [link_to_miniapp_ru]
])