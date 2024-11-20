from telegram import CallbackQuery, Bot

from bot.bot_api.config.message_text import TEXT_FOR_MESSAGES
from bot.bot_api.config.callback_names import CallbackNames

from bot.bot_api.keyboards.keyboards import back_to_this_message_keyboard

from bot.bot_api.bot_utils.logger import user_activity_logger


async def show_rest_info(flag: bool,
                         query: CallbackQuery,
                         bot: Bot,
                         chat_id: int,
                         rest_id: int,
                         user_id: int) -> None:
    # Выполняются запросы к БД

    text = TEXT_FOR_MESSAGES.get_text_for_rest_mes("Eboba", "Москва", "Патриарши пруды", "8")

    if flag:
        user_activity_logger.info(f"Пользователь {user_id} перешел на страницу ресторана {rest_id}")
    else:
        user_activity_logger.info(f"Пользователь {user_id} вернулся на страницу ресторана")


    await bot.send_message(chat_id=chat_id, text=text)
    if flag:
        await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
            CallbackNames.switch_to_rest_management
        ))
