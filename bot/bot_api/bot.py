from telegram.ext import ApplicationBuilder

from config import TOKEN

from bot_handlers import (start_command,
                          callback_query,
                          add_rest_conv_handler)

from bot_utils import error_handler


def main() -> None:
    bot1 = ApplicationBuilder().token(TOKEN).build()

    bot1.add_handler(start_command)
    bot1.add_handler(callback_query)
    bot1.add_handler(add_rest_conv_handler)

    bot1.add_error_handler(error_handler)

    bot1.run_polling()


if __name__ == "__main__":
    main()
