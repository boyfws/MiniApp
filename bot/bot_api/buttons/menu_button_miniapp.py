from telegram import MenuButtonWebApp
from bot.bot_api.bot_config import web_app_info
from bot.bot_api.buttons.buttons_settings.buttons_text import TEXT

menu_bottom_miniapp: MenuButtonWebApp = MenuButtonWebApp(text=TEXT.menu_button, web_app=web_app_info)
