from telegram.ext import CallbackQueryHandler
from telegram import Update
from telegram.ext import CallbackContext

from bot.bot_api.callback_names import CallbackNames

from bot.bot_api.keyboards.back_to_message import back_to_this_message_keyboard

from bot.bot_api.actions.switch_to_rest_man import switch_to_rest_man
from bot.bot_api.actions.create_new_rest import create_new_rest
from bot.bot_api.actions.send_start_message import send_start_message

from bot.bot_api.buttons_text import TEXT_FOR_BUTTONS


async def process_callback(update: Update, context: CallbackContext) -> None:
    """
    Отвечает за нажатие всех кнопок кроме кнопок ресторанов
    """
    query = update.callback_query
    await query.answer()
    first_button_text = query.message.reply_markup.inline_keyboard[0][0].text
    flag = first_button_text != TEXT_FOR_BUTTONS.back_to_message

    match query.data:

        case CallbackNames.switch_to_rest_management:
            await switch_to_rest_man(update=update, context=context)
            if flag:
                await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
                    CallbackNames.start
                ))

        case CallbackNames.create_new_rest:
            await create_new_rest(update=update, context=context)
            if flag:
                await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
                    CallbackNames.switch_to_rest_management
                ))

        case CallbackNames.start:
            await send_start_message(update=update, context=context)

    if not flag:
        await query.edit_message_reply_markup(reply_markup=None)


callback_query: CallbackQueryHandler = CallbackQueryHandler(process_callback, pattern=r'^[^\d]+$')
# Паттерн для строк, числа зарезервированы под рестораны
