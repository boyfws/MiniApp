from telegram.ext import CallbackQueryHandler, ContextTypes
from telegram import Update, CallbackQuery, Message
from typing import cast

from bot.bot_api.callback_names import CallbackNames

from bot.bot_api.buttons_text import TEXT_FOR_BUTTONS

from bot.bot_api.callback_hadlers.switch_to_rest_management import switch_to_rest_management
from bot.bot_api.callback_hadlers.create_new_rest import create_new_rest
from bot.bot_api.callback_hadlers.send_start_message import send_start_message
from bot.bot_api.callback_hadlers.show_rest_info import show_rest_info


async def process_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отвечает за нажатие всех кнопок кроме кнопок ресторанов
    """
    query = cast(CallbackQuery, update.callback_query)

    if update.effective_chat is None:
        return None
    """
    The chat that this update was sent in, no matter what kind of update this is. 
    If no chat is associated with this update, this gives None. This is the case, if inline_query, 
    chosen_inline_result, callback_query from inline messages, shipping_query, pre_checkout_query, poll, poll_answer, 
    business_connection, or purchased_paid_media is present.
    
    Changed in version 21.1: This property now also considers business_message, edited_business_message, and deleted_business_messages.
    """

    chat_id = update.effective_chat.id
    bot = context.bot
    await query.answer()

    message = cast(Message, query.message) # Мы не удаляем сообщение, а оно не удалено, так как кнопка была нажата

    if message.reply_markup is None:
        return None

    first_button_text = message.reply_markup.inline_keyboard[0][0].text
    flag = first_button_text != TEXT_FOR_BUTTONS.back_to_message

    if query.data is None: # Доп чек
        return None

    match query.data:
        case CallbackNames.switch_to_rest_management:
            await switch_to_rest_management(flag=flag, query=query, chat_id=chat_id, bot=bot)

        case CallbackNames.create_new_rest:
            await create_new_rest(flag=flag, query=query, chat_id=chat_id, bot=bot)

        case CallbackNames.start:
            await send_start_message(chat_id=chat_id, bot=bot)

    if ":" in query.data:
        # Чекаем колбэки с данными
        try:
            callback_name, arg = query.data.split(":")
        except ValueError:
            return None

        match callback_name:
            case CallbackNames.show_rest_info:
                await show_rest_info(query=query, flag=flag, bot=bot, chat_id=chat_id)

    if not flag:
        await query.edit_message_reply_markup(reply_markup=None)


callback_query = CallbackQueryHandler(process_callback)
