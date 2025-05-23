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
log_level = logging.DEBUG
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


commands = [
    BotCommand(command="/add_income", description="Add income"),
    BotCommand(command="/add_spending", description="Add spending"),
    # BotCommand(command="/today", description="Show today's expenses"),
    # BotCommand(command="/pocket", description="Show Pocket Money"),
    # BotCommand(command="/expenses", description="Show Expenses"),
    # BotCommand(command="/settings", description="Adjust your preferences"),
]

# Initialize a database
DATABASE_URL = os.getenv("DATABASE_URL")
