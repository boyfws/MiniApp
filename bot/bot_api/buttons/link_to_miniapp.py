from telegram import InlineKeyboardButton
from bot.bot_api.config.bot_config import web_app_info
from bot.bot_api.config.buttons_text import TEXT_FOR_BUTTONS

link_to_miniapp: InlineKeyboardButton = InlineKeyboardButton(TEXT_FOR_BUTTONS.link_to_miniapp_text, web_app=web_app_info)
