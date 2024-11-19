from telegram.ext import CallbackQueryHandler, ContextTypes
from telegram import Update, CallbackQuery, Message
from typing import cast

from bot.bot_api.config.callback_names import CallbackNames

from bot.bot_api.config.buttons_text import TEXT_FOR_BUTTONS

from bot.bot_api.callback_handlers.switch_to_rest_management import switch_to_rest_management
from bot.bot_api.callback_handlers.send_start_message import send_start_message
from bot.bot_api.callback_handlers.show_rest_info import show_rest_info
from bot.bot_api.callback_handlers.show_that_buttons_are_unav_while_add_rest import \
    show_that_buttons_are_unav_while_add_rest as buttons_are_unav

from bot.bot_api.bot_utils.logger import user_activity_logger, injection_notifier_logger


async def process_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отвечает за нажатие всех кнопок кроме кнопок ресторанов
    """
    query = cast(CallbackQuery, update.callback_query)
    await query.answer()

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
    user_id = update.effective_user.id

    message = cast(Message, query.message)  # Мы не удаляем сообщение, а оно не удалено, так как кнопка была нажата

    if message.reply_markup is None:
        return None

    first_button_text = message.reply_markup.inline_keyboard[0][0].text
    flag = first_button_text != TEXT_FOR_BUTTONS.back_to_message

    if query.data is None:  # Доп чек
        return None

    if context.user_data['in_conversation']:
        await buttons_are_unav(bot=bot, chat_id=chat_id)
        return None

    match query.data:
        case CallbackNames.switch_to_rest_management:
            await switch_to_rest_management(flag=flag, query=query, chat_id=chat_id, bot=bot, user_id=user_id)

            if flag:
                user_activity_logger.info(f"Пользователь {user_id} перешел на страницу управления ресторанами")
            else:
                user_activity_logger.info(f"Пользователь {user_id} вернулся на старицу управления ресторанами")

        case CallbackNames.start:
            await send_start_message(chat_id=chat_id, bot=bot)

            user_activity_logger.info(f"Пользователь вернулся на главную страницу")

    if ":" in query.data:
        # Чекаем колбэки с доп данными
        try:
            callback_name, arg = query.data.split(":")
        except ValueError:
            injection_notifier_logger.warning(
                f"От пользователя {user_id} поступил callback с двумя символами ':': {query.data}")
            return None

        match callback_name:
            case CallbackNames.show_rest_info:
                try:
                    rest_id = int(arg)
                except ValueError:
                    injection_notifier_logger.warning(
                        f"От пользователя {user_id} поступил callback с нечисловым id ресторана: {arg}")
                    return None

                await show_rest_info(query=query, flag=flag, bot=bot, chat_id=chat_id, rest_id=rest_id)

                if flag:
                    user_activity_logger.info(f"Пользователь {user_id} перешел на страницу ресторана {arg}")
                else:
                    user_activity_logger.info(f"Пользователь {user_id} вернулся на страницу ресторана")
    if not flag:
        await context.bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


callback_query = CallbackQueryHandler(process_callback, block=False, pattern=r'^[^_]+$')
# Проверяем, что в строке нет _, чтобы не перехватывать чужие колбэки 
