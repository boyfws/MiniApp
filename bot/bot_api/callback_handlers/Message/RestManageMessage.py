from bot_api.callback_handlers.Utils import QueryTools, UserValidation, ValidateArg

from telegram import Update
from telegram.ext import ContextTypes

from bot_api.config import (NamesForCallback,
                            TextForMessages)

from bot_api.keyboards import (back_to_this_message_keyboard,
                               rest_for_inheritance_keyboard)


class RestManageMessage(QueryTools,
                        UserValidation,
                        ValidateArg):
    def __init__(self):
        super().__init__()

    async def handle_rest_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query, chat_id, user_id, bot, message, flag = await self.prepare_data(update=update, context=context)

        args = self.get_args(query)
        if not self.validate_args(args=args,
                                  num_args=1,
                                  dtypes=[int],
                                  user_id=user_id):
            return None

        rest_id = int(args[0])

        if not await self.validate_user(rest_id=rest_id, user_id=user_id):
            return None

        text = TextForMessages.get_text_for_rest_mes("Eboba", "Москва", "Патриарши пруды", "8")

        self._log_handle_rest_click(user_id=user_id, flag=flag, rest_id=rest_id)

        await bot.send_message(chat_id=chat_id, text=text)
        if flag:
            await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
                NamesForCallback.switch_to_rest_management
            ))

        await self.delete_message(flag=flag,
                                  bot=bot,
                                  chat_id=chat_id,
                                  message_id=message.message_id)

        # Кнопка create new rest обрабатывается в inheriatnce, из-за особенностей
        # архитектуры фреймворка








