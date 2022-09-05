from config import config
import logging
from telegram_bot.handlers.commands import list_handlers


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


def main():
    config.application.add_handlers(list_handlers())
    #config.application.run_polling()


if __name__ == '__main__':
    main()
