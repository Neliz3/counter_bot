from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
import os
from dotenv import load_dotenv
import logging
import betterlogging as bl
import sys


# Initialize environment variables
load_dotenv()


# Logging setup
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=log_level,
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


# Initialize a bot
TOKEN = os.getenv("TOKEN")
storage = MemoryStorage()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage, bot=bot)


# Language setup
DEFAULT_LANG = "uk"
LANGUAGES = ("uk", "en")


# Setup commands | EN - UK languages support
commands = [
    BotCommand(command="/add_income", description="Додати дохід"),
    BotCommand(command="/add_spending", description="Додати витрати"),
    BotCommand(command="/today", description="Статистика за сьогодні"),
    BotCommand(command="/month", description="Статистика за місяць"),
    BotCommand(command="/cats", description="Змінити категорії"),
]


# Initialize a database
DATABASE_URL = os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
