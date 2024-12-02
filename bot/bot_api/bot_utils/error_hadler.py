from .logger import error_handler_logger
import telegram
from telegram import Update
from telegram.ext import ContextTypes
import traceback


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        raise context.error
    except telegram.error.TimedOut as e:
        error_handler_logger.error("Бот не смог установить соединение с сервером в течение заданного времени ожидания")
    except telegram.error.BadRequest as e:
        error_handler_logger.error(f"Возникла ошибка при при отправке запроса. Причина: {e.message}")
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        full_traceback = traceback.extract_tb(e.__traceback__)
        last_traceback = full_traceback[-1]
        error_handler_logger.critical(f"Необработанная ошибка: {error_type}. Сообщение: {error_message}. Путь: {last_traceback.filename}. Строка: {last_traceback.lineno}. Функция: {last_traceback.name}")
