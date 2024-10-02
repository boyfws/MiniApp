from telegram import InlineKeyboardMarkup

from ..buttons.link_to_miniapp_en import link_to_miniapp_en

start_keyboard_en: InlineKeyboardMarkup = InlineKeyboardMarkup([
    [link_to_miniapp_en]
])