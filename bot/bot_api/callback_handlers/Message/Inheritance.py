from bot_api.callback_handlers.Utils import (QueryTools,
                                             UserValidation,
                                             ValidateArg)
from telegram.ext import ContextTypes, ConversationHandler

from bot_api.external_api import (get_rest_properties,
                                  get_rest_name,
                                  get_user_rest)

from bot_api.config import *


from bot_api.keyboards import (inheritance_properties_keyboard,
                               back_to_this_message_keyboard,
                               rest_for_inheritance_keyboard,
                               inheritance_click_property_keyboard)

from bot_api.bot_utils import Update_mod


class Inheritance(QueryTools,
                  UserValidation,
                  ValidateArg):
    def __init__(self):
        super().__init__()

    async def create_new_rest(self, update: Update_mod, context: ContextTypes.DEFAULT_TYPE) -> int | None:
        query, chat_id, user_id, bot, message, flag = await self.prepare_data(update=update, context=context)

        restaurants = await get_user_rest(user_id=user_id)

        self._log_create_new_rest(user_id=user_id, flag=flag)

        if flag:
            context.user_data['in_conversation'] = True

        await bot.send_message(chat_id=chat_id,
                               text=TextForMessages.start_init_rest,
                               reply_markup=rest_for_inheritance_keyboard(restaurants))

        await query.edit_message_reply_markup(reply_markup=back_to_this_message_keyboard(
            NamesForCallback.switch_to_rest_management
        ))

        await self.delete_message(flag=flag,
                                  bot=bot,
                                  chat_id=chat_id,
                                  message_id=message.message_id)

        if not flag:
            return INHERITANCE
        else:
            # Пользователь мог нажать вернуться из любой точки диалога,
            # поэтому мы не должны возвращать state, чтобы не сбить conversation handler
            return None

    async def show_prop_for_inheritance(self,
                                        update: Update_mod,
                                        context: ContextTypes.DEFAULT_TYPE) -> None | int:
        query, chat_id, user_id, bot, message, flag = await self.prepare_data(update=update, context=context)
        args = self.get_args(query)
        if not self.validate_args(args=args, num_args=1, dtypes=[int], user_id=user_id):
            return None

        rest_id = int(args[0])

        if not await self.validate_user(rest_id=rest_id, user_id=user_id):
            return None

        rest_name = await get_rest_name(rest_id=rest_id)
        properties = await get_rest_properties(rest_id=rest_id)
        properties = tuple(el for el in properties if hasattr(PropInCallBack_INH, el))

        await bot.send_message(chat_id=chat_id,
                               text=TextForMessages.get_text_for_rest_mes_inheritance(rest_name),
                               reply_markup=inheritance_properties_keyboard(
                                   rest_id=rest_id,
                                   properties=properties)
                                )

        await self.add_back_buttons(flag=flag,
                                    query=query,
                                    callback_name=f"{NamesForCallback.adding_rest_conv_mark}_{NamesForCallback.create_new_rest}")

        await self.delete_message(flag=flag,
                                  bot=bot,
                                  chat_id=chat_id,
                                  message_id=message.message_id)
        return INHERITANCE

    async def move_on_from_inheritance(self,
                                       update: Update_mod,
                                       context: ContextTypes.DEFAULT_TYPE) -> int:
        self._log_move_on_from_inheritance(user_id=update.effective_user.id)
        return NAME

    async def stop_rest_adding_conv(self,
                                    update: Update_mod,
                                    context: ContextTypes.DEFAULT_TYPE) -> int | None:
        query, chat_id, user_id, bot, message, flag = await self.prepare_data(update=update, context=context)
        if context.user_data['in_conversation']:
            self._log_stop_rest_add_conv(user_id=user_id)
            context.user_data['in_conversation'] = False
            return ConversationHandler.END
        else:
            # Если мы не в диалоге игнорим
            return None

    async def handle_property_click(self, update: Update_mod, context: ContextTypes.DEFAULT_TYPE) -> int | None:
        query, chat_id, user_id, bot, message, flag = await self.prepare_data(update=update, context=context)
        args = self.get_args(query)
        if not self.validate_args(args, num_args=2, dtypes=[int, str], user_id=user_id):
            return None
        rest_id, prop = args
        rest_id = int(rest_id)

        if not await self.validate_user(user_id=user_id, rest_id=rest_id):
            return None

        rest_name = await get_rest_name(rest_id=rest_id)
        await bot.send_message(chat_id=chat_id,
                               text=TextForMessages.get_text_for_mes_show_confirm_inh(prop, rest_name),
                               reply_markup=inheritance_click_property_keyboard(rest_id=rest_id,
                                                                                property=prop)
                               )

        await self.add_back_buttons(flag=flag,
                                    query=query,
                                    callback_name=f"{NamesForCallback.adding_rest_conv_mark}_{NamesForCallback.inheritance_property_of_rest}:{rest_id}")









