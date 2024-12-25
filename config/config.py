from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
import os
from dotenv import load_dotenv
import logging
import sys

# Initialize environment variables
load_dotenv()


# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout,
)


# Initialize a bot
TOKEN = os.getenv("TOKEN")
storage = MemoryStorage()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage, bot=bot)


commands = [
    BotCommand(command="/start", description="Start the bot"),
    BotCommand(command="/pocket", description="Show Pocket Money"),
    BotCommand(command="/expenses", description="Show Expenses"),
    BotCommand(command="/table", description="Get Google Spreadsheet link"),
    BotCommand(command="/settings", description="Adjust your preferences"),
]

# Initialize admin
admin = os.getenv("ADMIN")

# Initialize a database
db_name = 'users.db'

# Initialize lists of categories
categories = {
    'key_income': ['income', 'salary'],
    'key_apartment': ['room', 'utilities'],
    'key_phone': ['phone', 'mob', 'mobile'],
    'key_nutrition': ['food', 'eat', 'cafe', 'restaurant', 'atb'],
    'key_education': ['book', 'books', 'course', 'certificate', 'english', 'lesson'],
    'key_health': ['health', 'hygiene', 'pharmacy', 'vitamins', 'doc', 'doctor'],
    'key_transport': ['bus', 'trolleybus', 'tram', 'train', 'plane',
                      'aircraft', 'airplane', 'taxi', 'tickets'],
    'key_clothing': ['clothing', 'clothes', 'wear'],
    'key_house': ['home', 'trinket'],
    'key_travelling': ['travel', 'journey', 'trip']
}

# Initialize links
template_spreadsheet_url = ('https://docs.google.com/spreadsheets/d/'
                      '1C-Z0OPYnyKPSjn8_YvrpE4uFIPiw0xQrSTn2OHhPVO4/'
                      'edit#gid=1785411570')
