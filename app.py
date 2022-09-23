from config import config
import logging
from telegram_bot.handlers.commands import list_handlers
from google_sheets.authentication.auth import list_handlers_auth


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    config.application.add_handlers(list_handlers())
    config.application.add_handler(list_handlers_auth())
    config.application.run_polling()


if __name__ == '__main__':
    main()
