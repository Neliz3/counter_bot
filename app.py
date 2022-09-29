from config import config
import logging
from telegram_bot.handlers.commands import list_commands
from telegram_bot.handlers.callback_query import list_query


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    config.application.add_handlers(list_commands())
    config.application.add_handler(list_query())
    config.application.run_polling()


if __name__ == '__main__':
    main()
