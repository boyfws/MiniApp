from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from bot.buttons.menu_button_miniapp_en import menu_bottom_miniapp_en
from bot.buttons.menu_button_miniapp_ru import menu_bottom_miniapp_ru

from bot.keyboards.start_keyboard_en import start_keyboard_en
from bot.keyboards.start_keyboard_ru import start_keyboard_ru

lang_of_response_text = {"ru": "Привет!",
                         "en": "Hi"
                         }


async def start(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает команду инициализации бота, вывыодя пользователю приветсвенное сообщение
    с кнопкой для перехода в мини приложение, также создает кнопку для перехода в мини приложение
    В зависимсоти от языка пользователя меняет язык приветсвенного сообщения и мини приложения,
    если язык не известен - используется русский
    """
    chat_id = update.effective_chat.id
    if update.message.from_user.language_code == "en":
        response_text = lang_of_response_text["en"]
        response_keyboard = start_keyboard_en
        menu_bottom = menu_bottom_miniapp_en
    else:
        response_text = lang_of_response_text["ru"]
        response_keyboard = start_keyboard_ru
        menu_bottom = menu_bottom_miniapp_ru

    await context.bot.set_chat_menu_button(chat_id=chat_id, menu_button=menu_bottom)
    await update.message.reply_text(response_text, reply_markup=response_keyboard)


start_command: CommandHandler = CommandHandler("start", start)