from telegram import CallbackQuery, Bot

from bot_api.config import (TextForMessages,
                            NamesForCallback)

from bot_api.keyboards import back_to_this_message_keyboard

from bot_api.bot_utils import user_activity_logger


async def handle_rest_click_on_rest_manage_message(flag: bool,
                                                   query: CallbackQuery,
                                                   bot: Bot,
                                                   chat_id: int,
                                                   rest_id: int,
                                                   user_id: int) -> None:
    # Выполняются запросы к БД

    text = TextForMessages.get_text_for_rest_mes("Eboba", "Москва", "Патриарши пруды", "8")

    if flag:
        user_activity_logger.info(f"Пользователь {user_id} перешел на страницу ресторана {rest_id}")
    else:
        user_activity_logger.info(f"Пользователь {user_id} вернулся на страницу ресторана")


    await bot.send_message(chat_id=chat_id, text=text)
    if flag:
        await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
            NamesForCallback.switch_to_rest_management
        ))
