from bot_api.external_api import (check_user_roots,
                                  get_rest_properties,
                                  get_rest_name)

from bot_api.config import (TextForMessages,
                            NamesForCallback)

from bot_api.bot_utils import injection_notifier_logger

from bot_api.keyboards import (inheritance_properties_keyboard,
                               back_to_this_message_keyboard)

from telegram import Bot, CallbackQuery


async def show_prop_for_inheritance(rest_id: int,
                                    user_id: int,
                                    bot: Bot,
                                    chat_id: int,
                                    flag: bool,
                                    query: CallbackQuery) -> None:
    if not await check_user_roots(user_id=user_id, rest_id=rest_id):
        injection_notifier_logger.error(
            f"Пользователь {user_id} попытался получить доступ не к своему ресторану {rest_id}"
        )
        return None
    rest_name = await get_rest_name(rest_id=rest_id)
    properties = await get_rest_properties(rest_id=rest_id)
    await bot.send_message(chat_id=chat_id,
                           text=TextForMessages.get_text_for_rest_mes_inheritance(rest_name),
                           reply_markup=inheritance_properties_keyboard(
                               rest_id=rest_id,
                               properties=properties)
                           )

    if flag:
        await query.edit_message_reply_markup(reply_markup=
        back_to_this_message_keyboard(
            f"{NamesForCallback.adding_rest_conv_mark}_{NamesForCallback.create_new_rest}"
        )
        )

