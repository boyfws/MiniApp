from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

from bot.bot_api.callback_handlers.stop_adding_rest_conv import stop_adding_rest_conv

from bot.bot_api.config.callback_names import CallbackNames


async def stop_conv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    if "state" in context.user_data:
        return await stop_adding_rest_conv


stop_conversation = CallbackQueryHandler(stop_conv,
                                         pattern=rf'^({CallbackNames.stop_rest_adding})$',
                                         block=False)
