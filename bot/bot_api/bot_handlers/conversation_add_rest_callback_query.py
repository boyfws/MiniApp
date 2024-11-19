from telegram.ext import ContextTypes, CallbackQueryHandler, ConversationHandler
from telegram import Update

from bot.bot_api.config.callback_names import CallbackNames
from bot.bot_api.config.state_names_for_adding_rest import *

from bot.bot_api.bot_utils.logger import user_activity_logger, injection_notifier_logger

from bot.bot_api.callback_handlers.create_new_rest import create_new_rest
from bot.bot_api.callback_handlers.stop_adding_rest_conv import stop_adding_rest_conv


async def process_callbacks_for_rest_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    bot = context.bot

    try:
        arg = query.data.split("_")[1]
    except ValueError:
        injection_notifier_logger.warning(f"Пользователь {user_id} отправил callback с более чем одним символом '_'")
        return None

    match arg:
        case CallbackNames.switch_from_inheritance:
            user_activity_logger.info(f"Пользователь {user_id} закончил наследование свойств своих ресторанов")
            return NAME

        case CallbackNames.create_new_rest:
            await create_new_rest(query=query,
                                  chat_id=chat_id,
                                  bot=bot,
                                  user_id=user_id)
            context.user_data['in_conversation'] = True
            user_activity_logger.info(f"Пользователь {user_id} начал создание ресторана")

            return INHERITANCE

        case CallbackNames.stop_rest_adding:

            user_activity_logger.info(f"Пользователь {user_id} досрочно завершил добавление ресторана")

            if context.user_data['in_conversation']:
                await stop_adding_rest_conv()
                return ConversationHandler.END


conversation_add_rest_callback_query = CallbackQueryHandler(process_callbacks_for_rest_add,
                                                            pattern=rf'^{CallbackNames.adding_rest_conv_mark}_\w*$')
# Ловим только колбэки связанные с данным conversation
