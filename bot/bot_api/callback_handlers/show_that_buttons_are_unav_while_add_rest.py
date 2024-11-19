from telegram import Bot
from bot.bot_api.config.message_text import TextForMessages


async def show_that_buttons_are_unav_while_add_rest(bot: Bot, chat_id: int) -> None:
    await bot.send_message(chat_id=chat_id,
                           text=TextForMessages.notif_that_buttons_are_unclickable_while_adding_rest)