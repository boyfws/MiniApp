from telegram.ext import CallbackQueryHandler
from telegram import Update
from telegram.ext import CallbackContext

from bot.bot_api.buttons.buttons_settings.callback_names import CallbackNames

from bot.bot_api.keyboards.start.onClick.switch_to_rest_man import switch_to_rest_man
from bot.bot_api.keyboards.rest_manage.onClick.create_new_rest import create_new_rest
from bot.bot_api.keyboards.rest_manage.onClick.back_from_man_page import back_from_man_page


async def process_callback(update: Update, context: CallbackContext) -> None:
    """
    Отвечает за нажатие всех кнопок кроме кнопок ресторанов
    """
    query = update.callback_query
    await query.answer()
    match query.data:
        case CallbackNames.back_from_rest_man:
            await back_from_man_page(update=update, context=context)

        case CallbackNames.switch_to_rest_management:
            await switch_to_rest_man(update=update, context=context)

        case CallbackNames.create_new_rest:
            await create_new_rest(update=update, context=context)


callback_query: CallbackQueryHandler = CallbackQueryHandler(process_callback, pattern=r'^[^\d]+$')
# Паттерн для строк, числа зарезервированы под рестораны
