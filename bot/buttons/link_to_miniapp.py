from telegram import InlineKeyboardButton
from bot.bot_config import web_app_info

link_to_miniapp: InlineKeyboardButton = InlineKeyboardButton("Что то на русском", web_app=web_app_info)
