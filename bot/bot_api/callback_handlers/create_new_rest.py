from telegram import Bot, CallbackQuery

from telegram.ext import ContextTypes

from bot_api.config import (NamesForCallback,
                            TextForMessages)

from bot_api.keyboards import (back_to_this_message_keyboard,
                               rest_for_inheritance_keyboard)

from bot_api.external_api import get_user_rest

from bot_api.bot_utils import user_activity_logger


async def create_new_rest(query: CallbackQuery,
                          chat_id: int,
                          bot: Bot,
                          user_id: int,
                          context: ContextTypes.DEFAULT_TYPE,
                          flag: bool) -> None:
    # Тут какие-то действия
    restaurants = await get_user_rest(user_id=user_id)

    if not flag:
        user_activity_logger.info(f"Пользователь {user_id} вернулся к стартовой странице для наследования")
    else:
        context.user_data['in_conversation'] = True
        user_activity_logger.info(f"Пользователь {user_id} начал создание ресторана")

    await bot.send_message(chat_id=chat_id,
                           text=TextForMessages.start_init_rest,
                           reply_markup=rest_for_inheritance_keyboard(restaurants))
    await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
        NamesForCallback.switch_to_rest_management
    ))
