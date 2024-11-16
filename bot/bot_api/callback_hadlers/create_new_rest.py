from telegram import Bot, CallbackQuery

from bot.bot_api.callback_names import CallbackNames

from bot.bot_api.keyboards.back_to_message import back_to_this_message_keyboard


async def create_new_rest(flag: bool, query: CallbackQuery, chat_id: int, bot: Bot) -> None:
    # Тут какие-то действия
    if flag:
        await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
            CallbackNames.switch_to_rest_management
        ))