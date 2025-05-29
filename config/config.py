from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from sqlalchemy import create_engine, Engine
from motor.motor_asyncio import AsyncIOMotorClient
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
def get_bot() -> Bot:
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set")
    return Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def get_dp() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage(), bot=get_bot())
    return dp


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


# Initialize databases
def get_engine() -> Engine:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")
    return create_engine(db_url)


def get_mongo_client() -> AsyncIOMotorClient:
    mongo_url = os.getenv("MONGO_URI")
    if not mongo_url:
        raise ValueError("MONGO_URI environment variable not set")
    return AsyncIOMotorClient(mongo_url)


def get_mongo_db_name() -> str:
    mongo_db_name = os.getenv("MONGO_DB_NAME")
    if not mongo_db_name:
        raise ValueError("MONGO_DB_NAME environment variable not set")
    return mongo_db_name
