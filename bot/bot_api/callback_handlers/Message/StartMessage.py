from bot_api.callback_handlers.Utils.QueryTools import QueryTools
from telegram.ext import ContextTypes

from bot_api.external_api import get_user_rest
from bot_api.config import (NamesForCallback,
                            TextForMessages)

from bot_api.keyboards import (back_to_this_message_keyboard,
                               get_rest_management_keyboard,
                               start_keyboard)


from bot_api.bot_utils import user_activity_logger, Update_mod


class StartMessage(QueryTools):
    def __init__(self):
        super().__init__()

    async def switch_to_rest_management(self,
                                        update: Update_mod,
                                        context: ContextTypes.DEFAULT_TYPE) -> None:

        query, chat_id, user_id, bot, message, flag = await self.prepare_data(update=update, context=context)

        rest_for_user = await get_user_rest(user_id=user_id)
        rest_manage_keyboard = get_rest_management_keyboard(rest_for_user)
        await bot.send_message(chat_id=chat_id,
                               text=TextForMessages.rest_management,
                               reply_markup=rest_manage_keyboard)

        self._log_switch_to_rest_management(flag=flag, user_id=user_id)

        await self.add_back_buttons(flag=flag,
                                    query=query,
                                    callback_name=NamesForCallback.start)

        await self.delete_message(flag=flag,
                                  bot=bot,
                                  chat_id=chat_id,
                                  message_id=message.message_id)

    async def back_to_start_message(self,
                                    update: Update_mod,
                                    context: ContextTypes.DEFAULT_TYPE) -> None:
        # Мы можем попасть на стартовое сообщение только через команду "Вернуться назад"
        query, chat_id, user_id, bot, message, flag = await self.prepare_data(update=update, context=context)
        await bot.send_message(chat_id=chat_id, text=TextForMessages.start, reply_markup=start_keyboard)
        user_activity_logger.info(f"Пользователь вернулся на главную страницу")
        await self.delete_message(flag=flag,
                                  bot=bot,
                                  chat_id=chat_id,
                                  message_id=message.message_id)




