from telegram import CallbackQuery, Message, Bot
from telegram.ext import ContextTypes

from bot_api.config import TextForButtons

from typing import Tuple, cast

from .Logger import Logger

from bot_api.bot_utils import Update_mod, CallbackQuery_mod


class QueryTools(Logger):
    def __init__(self):
        pass

    @staticmethod
    async def prepare_data(update: Update_mod,
                           context: ContextTypes.DEFAULT_TYPE) \
            -> Tuple[
                CallbackQuery_mod,
                int,
                int,
                Bot,
                Message,
                bool
            ]:
        query = update.callback_query
        #await query.answer()
        # Мы отвечаем на query на более высоком уровне

        chat_id = update.effective_chat.id
        bot = context.bot
        user_id = update.effective_user.id
        message = query.message

        first_button_text = message.reply_markup.inline_keyboard[0][0].text
        flag = first_button_text != TextForButtons.back_to_message

        return (query,
                chat_id,
                user_id,
                bot,
                message,
                flag)

    @staticmethod
    async def delete_message(flag: bool,
                             bot: Bot,
                             chat_id: int,
                             message_id: int) -> None:
        if not flag:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)



