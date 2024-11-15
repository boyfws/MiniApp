from telegram import InlineKeyboardMarkup

from bot.bot_api.buttons.link_to_miniapp import link_to_miniapp
from bot.bot_api.buttons.switch_to_rest_manage import switch_to_rest_management

start_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup([
    [link_to_miniapp],
    [switch_to_rest_management]
])