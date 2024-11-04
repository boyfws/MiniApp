from venv import logger

from telegram import Update, Message
from telegram.ext import CallbackContext, CommandHandler

from bot.buttons.menu_button_miniapp import menu_bottom_miniapp

from bot.keyboards.start_keyboard import start_keyboard
from bot.bot_utils.logger import start_logger

response_text = "Привет дружок"


async def start(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает команду инициализации бота, вывыодя пользователю приветсвенное сообщение
    с кнопкой для перехода в мини приложение, также создает кнопку для перехода в мини приложение
    """
    chat_id = update.effective_chat.id
    start_logger.info(f"Пришло сообщение от пользователя {update.message.from_user.id}")
    resp_of_button_set: bool = await context.bot.set_chat_menu_button(chat_id=chat_id,
                                                                      menu_button=menu_bottom_miniapp)
    if not resp_of_button_set:
        start_logger.error(f"При установке кнопки пользователю {update.message.from_user.id} возникла ошибка")
    resp_of_mes_sent: Message = await update.message.reply_text(response_text, reply_markup=start_keyboard)
    if resp_of_mes_sent.text != response_text:
        start_logger.error(f"При отправке сообщения пользователю {update.message.from_user.id} возникла ошибка")


start_command: CommandHandler = CommandHandler("start", start)
