from telegram.ext import ContextTypes, CallbackQueryHandler, ConversationHandler
from telegram import Update, Bot, CallbackQuery

from bot_api.config import *

from bot_api.bot_utils import injection_notifier_logger

from bot_api.callback_handlers import (create_new_rest,
                                       stop_rest_add_conv,
                                       show_prop_for_inheritance,
                                       switch_from_inheritance)


async def delete_message(flag: bool,
                         chat_id: int,
                         bot: Bot,
                         query: CallbackQuery) -> None:
    if not flag:
        await bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)


async def process_callbacks_for_rest_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    bot = context.bot

    first_button_text = query.message.reply_markup.inline_keyboard[0][0].text
    flag = first_button_text != TextForButtons.back_to_message

    try:
        callback = query.data.split("_")[1]
    except ValueError:
        injection_notifier_logger.warning(f"Пользователь {user_id} отправил callback с более чем одним символом '_'")
        return None

    match callback:
        case NamesForCallback.switch_from_inheritance:
            await switch_from_inheritance(user_id=user_id)
            return NAME

        case NamesForCallback.create_new_rest:
            await create_new_rest(query=query,
                                  chat_id=chat_id,
                                  bot=bot,
                                  user_id=user_id,
                                  context=context,
                                  flag=flag)
            await delete_message(flag=flag, chat_id=chat_id, bot=bot, query=query)
            if not flag:
                return INHERITANCE
            else:
                return None

        case NamesForCallback.stop_rest_adding:

            if context.user_data['in_conversation']:
                await stop_rest_add_conv(user_id=user_id)
                return ConversationHandler.END
            else:
                return None

    if ":" in callback:
        try:
            clear_callback, arguments = callback.split(":")
        except ValueError:
            injection_notifier_logger.warning(
                f"Пользователь {user_id} передал callback с более чем одним символом ':': {callback}")
            return None

        match clear_callback:
            case NamesForCallback.inheritance_property_of_rest:
                try:
                    rest_id = int(arguments)
                except ValueError:
                    injection_notifier_logger.warning(
                        f"Пользователь {user_id} передал неправильный id ресторана: {arguments}")
                    return None

                await show_prop_for_inheritance(rest_id=rest_id,
                                                user_id=user_id,
                                                bot=bot,
                                                chat_id=chat_id,
                                                flag=flag,
                                                query=query)
                await delete_message(flag=flag, chat_id=chat_id, bot=bot, query=query)
                return INHERITANCE


add_rest_conv_callback_query = CallbackQueryHandler(process_callbacks_for_rest_add,
                                                    pattern=rf'^{NamesForCallback.adding_rest_conv_mark}_[\w:,]*$')
# Ловим только колбэки связанные с данным conversation
