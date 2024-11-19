from bot.bot_api.config.message_text import TEXT_FOR_MESSAGES
from telegram.ext import ConversationHandler


async def stop_adding_rest_conv() -> int:
    return ConversationHandler.END
