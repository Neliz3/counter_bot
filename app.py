from telegram_bot.config import config
import logging
from telegram_bot.handlers.commands import list_handlers
from server.heroku_server import launch_server


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    config.application.add_handlers(list_handlers())
    launch_server()


if __name__ == '__main__':
    main()
