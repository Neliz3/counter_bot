from config import application
import logging
from handlers.commands import list_handlers


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    application.add_handlers(list_handlers())
    application.run_polling()


if __name__ == '__main__':
    main()
