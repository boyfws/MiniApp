from telegram.ext import ApplicationBuilder
import asyncio

from bot_config import TOKEN
from handlers.start_command import start_command

def main() -> None:
    bot1 = ApplicationBuilder().token(TOKEN).build()
    bot1.add_handler(start_command)

    bot1.run_polling()


if __name__ == "__main__":
    main()
