from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ConversationHandler

from bot_api.keyboards import start_keyboard
from bot_api.config import TextForMessages

from bot_api.keyboards import menu_bottom_miniapp

from bot_api.bot_utils import user_activity_logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    """
    Обрабатывает команду start выводя сообщение с кнопкой для перехода в мини приложение и кнопкой
    для управления ресторанами. Также прерывает conversation для добавления ресторана
    :param update:
    :param context:
    :return:
    """
    if update.effective_chat is None or update.message is None or update.message.from_user is None:
        return None

    chat_id = update.effective_chat.id
    bot = context.bot

    user_activity_logger.info(f"Пользователь {update.message.from_user.id} нажал start")

    context.user_data['in_conversation'] = False

    resp_of_button_set: bool = await bot.set_chat_menu_button(chat_id=chat_id,
                                                              menu_button=menu_bottom_miniapp)
    await bot.send_message(chat_id=chat_id, text=TextForMessages.start, reply_markup=start_keyboard)
    return ConversationHandler.END


start_command = CommandHandler("start", start)
