from telegram.ext import (ContextTypes,
                          CallbackQueryHandler)

from bot_api.config import NamesForCallback

from bot_api.bot_utils import val_callback_from_conv, val_callback_with_args, Update_mod

from bot_api.callback_handlers import ConvCallBackHandlers


callback_handler = ConvCallBackHandlers()


async def process_callbacks_for_rest_add(update: Update_mod, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    query = update.callback_query
    await query.answer()

    callback = val_callback_from_conv(query=query, update=update)
    if callback is None:
        return None

    match callback:
        case NamesForCallback.switch_from_inheritance:
            return await callback_handler.move_on_from_inheritance(update=update,
                                                                   context=context)

        case NamesForCallback.create_new_rest:
            return await callback_handler.create_new_rest(update=update,
                                                          context=context)

        case NamesForCallback.stop_rest_adding:
            return await callback_handler.stop_rest_adding_conv(update=update,
                                                                context=context)

    if ":" in callback:
        clear_callback, arguments = val_callback_with_args(query=query, update=update)

        if clear_callback is None or arguments is None:
            return None

        match clear_callback:
            case NamesForCallback.inheritance_property_of_rest:
                return await callback_handler.show_prop_for_inheritance(update=update,
                                                                        context=context)
    return None


add_rest_conversation_callback_query = CallbackQueryHandler(process_callbacks_for_rest_add,
                                                            pattern=rf'^{NamesForCallback.adding_rest_conv_mark}_[\w:,]*$')
# Ловим только колбэки связанные с данным conversation
