from telegram import CallbackQuery, Bot

from bot.bot_api.config.message_text import TEXT_FOR_MESSAGES
from bot.bot_api.config.callback_names import CallbackNames

from bot.bot_api.keyboards.keyboards import back_to_this_message_keyboard


async def show_rest_info(flag: bool, query: CallbackQuery, bot: Bot, chat_id: int) -> None:
    # Выполняются запросы к БД

    text = TEXT_FOR_MESSAGES.get_text_for_rest_mes("Eboba", "Москва", "Патриарши пруды", "8")
    await bot.send_message(chat_id=chat_id, text=text)
    if flag:
        await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
            CallbackNames.switch_to_rest_management
        ))
