from telegram import CallbackQuery, Bot

from bot.bot_api.callback_names import CallbackNames

from bot.bot_api.keyboards.back_to_message import back_to_this_message_keyboard

from bot.bot_api.message_text import TEXT_FOR_MESSAGES
from bot.bot_api.keyboards.rest_manage_keyboard import get_rest_man_keyboard


async def switch_to_rest_management(flag: bool, query: CallbackQuery, chat_id: int, bot: Bot) -> None:
    # Запрашиваем данные
    example_data = [("Уебар", 1), ("ДЛИИИИИИИИИИИИИИИИИИИИИИННННАЯ ХУИТА", 2), ("sdada", 0)]
    rest_manage_keyboard = get_rest_man_keyboard(example_data)
    await bot.send_message(chat_id=chat_id,
                           text=TEXT_FOR_MESSAGES.rest_management,
                           reply_markup=rest_manage_keyboard)

    if flag:
        await query.edit_message_reply_markup(
            reply_markup=back_to_this_message_keyboard(
                CallbackNames.start)
        )
