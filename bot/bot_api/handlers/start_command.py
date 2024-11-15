from telegram import Update, Message
from telegram.ext import CallbackContext, CommandHandler

from bot.bot_api.buttons.menu_button_miniapp import menu_bottom_miniapp
from bot.bot_api.keyboards.start.start_keyboard import start_keyboard

from bot.bot_api.bot_utils.logger import start_logger

from bot.bot_api.message_text import TEXT


async def start(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает команду инициализации бота, вывыодя пользователю приветсвенное сообщение
    с кнопкой для перехода в мини приложение, также создает кнопку для перехода в мини приложение
    """
    chat_id = update.effective_chat.id

    start_logger.info(f"Пользоавтель {update.message.from_user.id} нажал start")

    resp_of_button_set: bool = await context.bot.set_chat_menu_button(chat_id=chat_id,
                                                                      menu_button=menu_bottom_miniapp)
    resp_of_mes_sent: Message = await update.message.reply_text(TEXT.start, reply_markup=start_keyboard)


start_command: CommandHandler = CommandHandler("start", start)
