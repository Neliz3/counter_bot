from config import config
import logging
from telegram_bot.handlers.commands import list_commands


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    config.application.add_handlers(list_commands())
    config.application.run_polling()


if __name__ == '__main__':
    main()

# TODO bot will create its own table with all values, user need only click start and auth
