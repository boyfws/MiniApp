from telegram import CallbackQuery, Bot

from bot.bot_api.config.callback_names import CallbackNames

from bot.bot_api.keyboards.keyboards import back_to_this_message_keyboard

from bot.bot_api.config.message_text import TEXT_FOR_MESSAGES
from bot.bot_api.keyboards.keyboards import get_rest_management_keyboard

from bot.bot_api.external_api.get_user_rest import get_user_rest


async def switch_to_rest_management(flag: bool, query: CallbackQuery, chat_id: int, bot: Bot, user_id: int) -> None:
    rest_for_user = await get_user_rest(user_id=user_id)
    rest_manage_keyboard = get_rest_management_keyboard(rest_for_user)
    await bot.send_message(chat_id=chat_id,
                           text=TEXT_FOR_MESSAGES.rest_management,
                           reply_markup=rest_manage_keyboard)

    if flag:
        await query.edit_message_reply_markup(
            reply_markup=back_to_this_message_keyboard(
                CallbackNames.start)
        )
