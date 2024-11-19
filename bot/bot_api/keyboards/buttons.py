from bot.bot_api.config.buttons_text import TEXT_FOR_BUTTONS
from bot.bot_api.config.callback_names import CallbackNames
from telegram import InlineKeyboardButton

from telegram import MenuButtonWebApp

from bot.bot_api.config.bot_config import web_app_info

create_new_rest = InlineKeyboardButton(text=TEXT_FOR_BUTTONS.create_new_rest,
                                       callback_data=f"{CallbackNames.adding_rest_conv_mark}_{CallbackNames.create_new_rest}")

link_to_miniapp: InlineKeyboardButton = InlineKeyboardButton(TEXT_FOR_BUTTONS.link_to_miniapp_text,
                                                             web_app=web_app_info)

menu_bottom_miniapp: MenuButtonWebApp = MenuButtonWebApp(text=TEXT_FOR_BUTTONS.menu_button,
                                                         web_app=web_app_info)

stop_adding_rest = InlineKeyboardButton(text=TEXT_FOR_BUTTONS.stop_rest_adding,
                                        callback_data=f"{CallbackNames.adding_rest_conv_mark}_{CallbackNames.stop_rest_adding}")

switch_to_rest_management: InlineKeyboardButton = InlineKeyboardButton(text=TEXT_FOR_BUTTONS.switch_to_rest_management,
                                                                       callback_data=CallbackNames.switch_to_rest_management)


switch_from_inheritance = InlineKeyboardButton(text=TEXT_FOR_BUTTONS.switch_from_inheritance,
                                               callback_data=f"{CallbackNames.adding_rest_conv_mark}_{CallbackNames.switch_from_inheritance}")

