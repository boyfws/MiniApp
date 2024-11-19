from telegram import MenuButtonWebApp
from bot.bot_api.config.bot_config import web_app_info
from bot.bot_api.config.buttons_text import TEXT_FOR_BUTTONS

menu_bottom_miniapp: MenuButtonWebApp = MenuButtonWebApp(text=TEXT_FOR_BUTTONS.menu_button, web_app=web_app_info)
