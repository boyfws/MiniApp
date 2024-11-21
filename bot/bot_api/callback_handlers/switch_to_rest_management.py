from telegram import CallbackQuery, Bot

from bot_api.config import (NamesForCallback,
                            TextForMessages)

from bot_api.keyboards import (back_to_this_message_keyboard,
                               get_rest_management_keyboard)

from bot_api.external_api import get_user_rest

from bot_api.bot_utils import user_activity_logger


async def switch_to_rest_management(flag: bool, query: CallbackQuery, chat_id: int, bot: Bot, user_id: int) -> None:
    rest_for_user = await get_user_rest(user_id=user_id)
    rest_manage_keyboard = get_rest_management_keyboard(rest_for_user)
    await bot.send_message(chat_id=chat_id,
                           text=TextForMessages.rest_management,
                           reply_markup=rest_manage_keyboard)

    if flag:
        user_activity_logger.info(f"Пользователь {user_id} перешел на страницу управления ресторанами")
    else:
        user_activity_logger.info(f"Пользователь {user_id} вернулся на старицу управления ресторанами")

    if flag:
        await query.edit_message_reply_markup(
            reply_markup=back_to_this_message_keyboard(
                NamesForCallback.start)
        )
