from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from bot.bot_api.keyboards.buttons import menu_bottom_miniapp

from bot.bot_api.bot_utils.logger import start_logger
from bot.bot_api.callback_handlers.send_start_message import send_start_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает команду инициализации бота, вывыодя пользователю приветсвенное сообщение
    с кнопкой для перехода в мини приложение, также создает кнопку для перехода в мини приложение
    """
    if update.effective_chat is None or update.message is None or update.message.from_user is None:
        return None

    chat_id = update.effective_chat.id
    bot = context.bot

    start_logger.info(f"Пользоавтель {update.message.from_user.id} нажал start")

    resp_of_button_set: bool = await bot.set_chat_menu_button(chat_id=chat_id,
                                                              menu_button=menu_bottom_miniapp)
    await send_start_message(chat_id=chat_id, bot=bot)


start_command = CommandHandler("start", start)