from telegram.ext import ContextTypes, CallbackQueryHandler, ConversationHandler
from telegram import Update

from bot.bot_api.config.callback_names import CallbackNames
from bot.bot_api.config.state_names_for_rest_add_conv import *

from bot.bot_api.bot_utils.logger import user_activity_logger, injection_notifier_logger

from bot.bot_api.callback_handlers.create_new_rest import create_new_rest
from bot.bot_api.callback_handlers.stop_rest_add_conv import stop_rest_add_conv
from bot.bot_api.callback_handlers.show_prop_for_inheritance import show_prop_for_inheritance

from bot.bot_api.config.buttons_text import TEXT_FOR_BUTTONS


async def process_callbacks_for_rest_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    bot = context.bot

    first_button_text = query.message.reply_markup.inline_keyboard[0][0].text
    flag = first_button_text != TEXT_FOR_BUTTONS.back_to_message

    try:
        callback = query.data.split("_")[1]
    except ValueError:
        injection_notifier_logger.warning(f"Пользователь {user_id} отправил callback с более чем одним символом '_'")
        return None

    match callback:
        case CallbackNames.switch_from_inheritance:
            user_activity_logger.info(f"Пользователь {user_id} закончил наследование свойств своих ресторанов")
            return NAME

        case CallbackNames.create_new_rest:
            await create_new_rest(query=query,
                                  chat_id=chat_id,
                                  bot=bot,
                                  user_id=user_id)

            if flag:
                user_activity_logger.info(f"Пользователь {user_id} вернулся к стартовой странице для наследования")
            else:
                context.user_data['in_conversation'] = True
                user_activity_logger.info(f"Пользователь {user_id} начал создание ресторана")

                return INHERITANCE

        case CallbackNames.stop_rest_adding:

            user_activity_logger.info(f"Пользователь {user_id} досрочно завершил добавление ресторана")

            if context.user_data['in_conversation']:
                await stop_rest_add_conv()
                return ConversationHandler.END

    if ":" in callback:
        try:
            clear_callback, arguments = callback.split(":")
        except ValueError:
            injection_notifier_logger.warning(
                f"Пользователь {user_id} передал callback с более чем одним символом ':': {callback}")
            return None

        match clear_callback:
            case CallbackNames.inheritance_property_of_rest:
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
                return INHERITANCE


add_rest_conv_callback_query = CallbackQueryHandler(process_callbacks_for_rest_add,
                                                    pattern=rf'^{CallbackNames.adding_rest_conv_mark}_[\w:,]*$')
# Ловим только колбэки связанные с данным conversation
