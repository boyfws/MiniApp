from bot.bot_api.bot_utils.logger import error_handler_logger
import telegram
from telegram import Update
from telegram.ext import ContextTypes


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        raise context.error
    except telegram.error.TimedOut as e:
        error_handler_logger.error("Бот не смог установить соединение с сервером в течение заданного времени ожидания")
    except telegram.error.BadRequest as e:
        error_handler_logger.error(f"Возникла ошибка при при отправке запроса. Причина: {e.message}")
    except Exception as e:
        error_handler_logger.critical(f"Неизвестная ошибка: {e}")
