from telegram import Update
from telegram.ext import CallbackContext

from bot.bot_api.message_text import TEXT
from bot.bot_api.keyboards.rest_manage.rest_manage_keyboard import get_rest_man_keyboard


async def switch_to_rest_man(update: Update, context: CallbackContext) -> None:
    """
    Вызывается когда на главной странице пользователь нажал на кнопку для управления ресторанами
    Ему будут показаны его рестораны и кнопка для добавления нового ресторана
    """
    chat_id = update.effective_chat.id
    example_data = [("Уебар", 1), ("ДЛИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИИННННАЯ ХУИТА", 2), ("sdada", 0)]
    rest_manage_keyboard = get_rest_man_keyboard(example_data)
    await context.bot.send_message(chat_id=chat_id, text=TEXT.rest_management, reply_markup=rest_manage_keyboard)
