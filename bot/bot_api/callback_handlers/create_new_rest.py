from telegram import Bot, CallbackQuery

from telegram.ext import ContextTypes

from bot.bot_api.config.callback_names import CallbackNames
from bot.bot_api.config.message_text import TEXT_FOR_MESSAGES

from bot.bot_api.keyboards.keyboards import back_to_this_message_keyboard
from bot.bot_api.keyboards.keyboards import rest_for_inheritance_keyboard

from bot.bot_api.external_api.get_user_rest import get_user_rest

from bot.bot_api.bot_utils.logger import user_activity_logger


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
                           text=TEXT_FOR_MESSAGES.start_init_rest,
                           reply_markup=rest_for_inheritance_keyboard(restaurants))
    await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
        CallbackNames.switch_to_rest_management
    ))
