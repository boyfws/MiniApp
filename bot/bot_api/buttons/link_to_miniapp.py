from telegram import InlineKeyboardButton
from bot.bot_api.bot_config import web_app_info
from bot.bot_api.buttons.buttons_settings.buttons_text import TEXT

link_to_miniapp: InlineKeyboardButton = InlineKeyboardButton(TEXT.link_to_miniapp_text, web_app=web_app_info)
