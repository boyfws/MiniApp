from telegram import MenuButtonWebApp
from bot.bot_api.bot_config import web_app_info

menu_bottom_miniapp: MenuButtonWebApp = MenuButtonWebApp(text="Что-то на русском", web_app=web_app_info)
