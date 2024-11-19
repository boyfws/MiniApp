from telegram import Bot, CallbackQuery

from bot.bot_api.config.callback_names import CallbackNames

from bot.bot_api.keyboards.back_to_message import back_to_this_message_keyboard

from bot.bot_api.config.message_text import TEXT_FOR_MESSAGES


async def create_new_rest(query: CallbackQuery, chat_id: int, bot: Bot) -> None:
    # Тут какие-то действия
    await bot.send_message(chat_id=chat_id, text=TEXT_FOR_MESSAGES.start_init_rest)
    await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
        CallbackNames.switch_to_rest_management
    ))