from telegram.ext import ApplicationBuilder

from bot.bot_api.config.bot_config import TOKEN

from bot.bot_api.bot_handlers.start_command import start_command
from bot.bot_api.bot_handlers.callback_query import callback_query
from bot.bot_api.bot_handlers.conversation_handler import add_rest_conv


def main() -> None:
    bot1 = ApplicationBuilder().token(TOKEN).build()

    bot1.add_handler(start_command)
    bot1.add_handler(callback_query)
    bot1.add_handler(add_rest_conv)

    bot1.run_polling()


if __name__ == "__main__":
    main()
