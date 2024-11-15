from telegram.ext import ApplicationBuilder
import asyncio

from bot_config import TOKEN

from handlers.start_command import start_command
from handlers.callback_query import callback_query
from handlers.hadle_rest_click import rest_click


def main() -> None:
    bot1 = ApplicationBuilder().token(TOKEN).build()

    bot1.add_handler(start_command)
    bot1.add_handler(callback_query)
    bot1.add_handler(rest_click)

    bot1.run_polling()


if __name__ == "__main__":
    main()
