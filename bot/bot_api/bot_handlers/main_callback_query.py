from telegram.ext import CallbackQueryHandler, ContextTypes
from telegram import Update, CallbackQuery, Message
from typing import cast

from bot_api.config import NamesForCallback, TextForButtons

from bot_api.bot_utils import injection_notifier_logger

from bot_api.callback_handlers import (switch_to_rest_management,
                                       send_start_message,
                                       handle_rest_click_on_rest_manage_message,
                                       show_that_buttons_are_unav_while_add_rest as buttons_are_unav)


async def process_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отвечает за нажатие всех кнопок кроме кнопок ресторанов
    """
    query = cast(CallbackQuery, update.callback_query)
    await query.answer()

    if update.effective_chat is None:
        return None

    chat_id = update.effective_chat.id
    bot = context.bot
    user_id = update.effective_user.id

    message = cast(Message, query.message)  # Мы не удаляем сообщение, а оно не удалено, так как кнопка была нажата

    if message.reply_markup is None:
        return None

    first_button_text = message.reply_markup.inline_keyboard[0][0].text
    flag = first_button_text != TextForButtons.back_to_message

    if query.data is None:  # Доп чек
        return None

    if context.user_data['in_conversation']:
        await buttons_are_unav(bot=bot, chat_id=chat_id)
        return None

    match query.data:
        case NamesForCallback.switch_to_rest_management:
            await switch_to_rest_management(flag=flag, query=query, chat_id=chat_id, bot=bot, user_id=user_id)

        case NamesForCallback.start:
            await send_start_message(chat_id=chat_id, bot=bot, log=True)

    if ":" in query.data:
        # Чекаем колбэки с доп данными
        try:
            callback_name, arg = query.data.split(":")
        except ValueError:
            injection_notifier_logger.warning(
                f"От пользователя {user_id} поступил callback с двумя символами ':': {query.data}")
            return None

        match callback_name:
            case NamesForCallback.show_rest_info:
                try:
                    rest_id = int(arg)
                except ValueError:
                    injection_notifier_logger.warning(
                        f"От пользователя {user_id} поступил callback с нечисловым id ресторана: {arg}")
                    return None

                await handle_rest_click_on_rest_manage_message(query=query,
                                                               flag=flag,
                                                               bot=bot,
                                                               chat_id=chat_id,
                                                               rest_id=rest_id,
                                                               user_id=user_id)

    if not flag:
        await context.bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


callback_query = CallbackQueryHandler(process_callback, block=False, pattern=r'^[^_]+$')
# Проверяем, что в строке нет _, чтобы не перехватывать чужие колбэки
