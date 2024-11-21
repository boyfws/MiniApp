from bot_api.config import (TextForButtons,
                            NamesForCallback)

from telegram import InlineKeyboardButton

from telegram import MenuButtonWebApp

from bot_api.config import web_app_info

create_new_rest = InlineKeyboardButton(text=TextForButtons.create_new_rest,
                                       callback_data=f"{NamesForCallback.adding_rest_conv_mark}_{NamesForCallback.create_new_rest}")

link_to_miniapp: InlineKeyboardButton = InlineKeyboardButton(TextForButtons.link_to_miniapp_text,
                                                             web_app=web_app_info)

menu_bottom_miniapp: MenuButtonWebApp = MenuButtonWebApp(text=TextForButtons.menu_button,
                                                         web_app=web_app_info)

stop_rest_conv_button = InlineKeyboardButton(text=TextForButtons.stop_rest_adding,
                                             callback_data=f"{NamesForCallback.adding_rest_conv_mark}_{NamesForCallback.stop_rest_adding}")

switch_to_rest_management: InlineKeyboardButton = InlineKeyboardButton(text=TextForButtons.switch_to_rest_management,
                                                                       callback_data=NamesForCallback.switch_to_rest_management)


switch_from_inheritance = InlineKeyboardButton(text=TextForButtons.switch_from_inheritance,
                                               callback_data=f"{NamesForCallback.adding_rest_conv_mark}_{NamesForCallback.switch_from_inheritance}")

