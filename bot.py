from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp
import asyncio

from config import TOKEN, web_app_info_ru, web_app_info_eng

lang_select = {"ru": {"response_text": "Что то на русском",
                      "keyboard": [
                          [InlineKeyboardButton("Что то на русском", web_app=web_app_info_ru)]
                      ],
                      "menu_bottom": MenuButtonWebApp(text="Что-то на русском", web_app=web_app_info_ru)},
               "en": {"response_text": "Something on english",
                      "keyboard": [
                          [InlineKeyboardButton("Something on english", web_app=web_app_info_eng)]
                      ],
                      "menu_bottom": MenuButtonWebApp(text="Something on english", web_app=web_app_info_eng)}
               }


async def start(update: Update, context: CallbackContext) -> None:
    """
    Обрабатывает команду инициализации бота, вывыодя пользователю приветсвенное сообщение
    с кнопкой для перехода в мини приложение, также создает кнопку для перехода в мини приложение
    В зависимсоти от языка пользователя меняет язык приветсвенного сообщения и мини приложения
    """
    chat_id = update.effective_chat.id
    if update.message.from_user.language_code == "en":
        response_text = lang_select["en"]["response_text"]
        response_keyboard = lang_select["ru"]["keyboard"]
        menu_bottom = lang_select["en"]["menu_bottom"]
    else:
        response_text = lang_select["ru"]["response_text"]
        response_keyboard = lang_select["ru"]["keyboard"]
        menu_bottom = lang_select["ru"]["menu_bottom"]

    await context.bot.set_chat_menu_button(chat_id=chat_id, menu_button=menu_bottom)
    await update.message.reply_text(response_text, reply_markup=InlineKeyboardMarkup(response_keyboard))


def main() -> None:
    bot1 = ApplicationBuilder().token(TOKEN).build()
    bot1.add_handler(CommandHandler("start", start))

    bot1.run_polling()


if __name__ == "__main__":
    main()
