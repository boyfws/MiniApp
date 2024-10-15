from telegram import InlineKeyboardMarkup

from ..buttons.link_to_miniapp import link_to_miniapp

start_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup([
    [link_to_miniapp]
])