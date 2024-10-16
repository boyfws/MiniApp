from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from bot.buttons.menu_button_miniapp import menu_bottom_miniapp

from bot.keyboards.start_keyboard import start_keyboard

response_text = "Привет дружок"


async def start(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает команду инициализации бота, вывыодя пользователю приветсвенное сообщение
    с кнопкой для перехода в мини приложение, также создает кнопку для перехода в мини приложение
    """
    chat_id = update.effective_chat.id
    await context.bot.set_chat_menu_button(chat_id=chat_id, menu_button=menu_bottom_miniapp)
    await update.message.reply_text(response_text, reply_markup=start_keyboard)


start_command: CommandHandler = CommandHandler("start", start)