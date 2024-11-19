from telegram.ext import ContextTypes, CallbackQueryHandler, filters
from telegram import Update
from bot.bot_api.callback_handlers.create_new_rest import create_new_rest
from bot.bot_api.config.state_names_for_adding_rest import NAME
from bot.bot_api.config.callback_names import CallbackNames


async def create_new_rest_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await create_new_rest(query=update.callback_query, bot=context.bot, chat_id=update.effective_chat.id)
    return NAME

create_new_rest_start_point = CallbackQueryHandler(create_new_rest_handler, pattern=rf'^({CallbackNames.create_new_rest})$', block=False)
