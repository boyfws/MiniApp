from telegram.ext import CallbackQueryHandler, ContextTypes
from telegram import Update

from bot_api.config import NamesForCallback

from bot_api.bot_utils import val_callback_with_args
from bot_api.callback_handlers import CallBackHandlers

callback_handler = CallBackHandlers()


async def process_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отвечает за нажатие всех кнопок, кроме кнопок внутри conversation handler - ов
    """
    query = update.callback_query
    await query.answer()

    if context.user_data['in_conversation']:
        await callback_handler.show_that_other_buttons_are_unav_while_add_rest(update=update,
                                                                               context=context)
        return None

    match query.data:
        case NamesForCallback.switch_to_rest_management:
            await callback_handler.switch_to_rest_management(update=update,
                                                             context=context)
        case NamesForCallback.start:
            await callback_handler.back_to_start_message(update=update,
                                                         context=context)

    if ":" in query.data:
        callback_name, arg = val_callback_with_args(update=update, query=query)
        if callback_name is None or arg is None:
            return None

        match callback_name:
            case NamesForCallback.show_rest_info:
                await callback_handler.handle_rest_click(update=update,
                                                         context=context)


callback_query = CallbackQueryHandler(process_callback, block=False, pattern=r'^[^_]+$')
# Проверяем, что в строке нет _, чтобы не перехватывать чужие колбэки
