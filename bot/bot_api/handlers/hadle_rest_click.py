from telegram.ext import CallbackQueryHandler, CallbackContext
from telegram import Update

from bot.bot_api.keyboards.back_to_message import back_to_this_message_keyboard

from bot.bot_api.callback_names import CallbackNames

from bot.bot_api.buttons_text import TEXT_FOR_BUTTONS

from bot.bot_api.actions.show_rest_info import show_rest_info


async def handle_rest_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    await show_rest_info(update=update, context=context)

    first_button_text = query.message.reply_markup.inline_keyboard[0][0].text
    if first_button_text != TEXT_FOR_BUTTONS.back_to_message:
        await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
            CallbackNames.switch_to_rest_management
        ))
    else:
        await query.edit_message_reply_markup(reply_markup=None)


rest_click: CallbackQueryHandler = CallbackQueryHandler(handle_rest_click, pattern=r'^\d+$')
# Обрабатываем толко числа, выделены для номеров ресторанов
