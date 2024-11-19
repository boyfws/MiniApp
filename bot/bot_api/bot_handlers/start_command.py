from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ConversationHandler

from bot.bot_api.keyboards.buttons import menu_bottom_miniapp

from bot.bot_api.bot_utils.logger import user_activity_logger
from bot.bot_api.callback_handlers.send_start_message import send_start_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    """
    Обрабатывает команду инициализации бота, вывыодя пользователю приветсвенное сообщение
    с кнопкой для перехода в мини приложение, также создает кнопку для перехода в мини приложение
    """
    if update.effective_chat is None or update.message is None or update.message.from_user is None:
        return None

    chat_id = update.effective_chat.id
    bot = context.bot

    user_activity_logger.info(f"Пользоавтель {update.message.from_user.id} нажал start")

    context.user_data['in_conversation'] = False

    resp_of_button_set: bool = await bot.set_chat_menu_button(chat_id=chat_id,
                                                              menu_button=menu_bottom_miniapp)
    await send_start_message(chat_id=chat_id, bot=bot)
    return ConversationHandler.END


start_command = CommandHandler("start", start)
