from .QueryTools import QueryTools

from telegram.ext import ContextTypes
from bot_api.config import TextForMessages
from bot_api.bot_utils import Update_mod



class CommonTools(QueryTools):
    def __init__(self):
        super().__init__()

    async def show_that_other_buttons_are_unav_while_add_rest(self,
                                                        update: Update_mod,
                                                        context: ContextTypes.DEFAULT_TYPE) -> None:
        query, chat_id, user_id, bot, message, flag = await self.prepare_data(update=update, context=context)
        await bot.send_message(chat_id=chat_id,
                               text=TextForMessages.notif_that_buttons_are_unclickable_while_adding_rest)

