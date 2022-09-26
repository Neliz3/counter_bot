from telegram.ext import ApplicationBuilder
import os
from dotenv import load_dotenv


# Initialize environment variables
#load_dotenv('/home/elizabeth/counter_bot/config/.env')
load_dotenv()


# Initialize a bot
token_bot = os.getenv("TOKEN")
application = ApplicationBuilder().token(token_bot).build()


# Initialize admin
admin = os.getenv("ADMIN")


# Initialize a database
db_name = 'users.db'


# Initialize lists of categories
key_income = ['income', 'salary']
key_apartment = ['room', 'utilities']
key_phone = ['phone', 'mob', 'mobile']
key_nutrition = ['food', 'eat', 'cafe', 'restaurant', 'atb']
key_education = ['book', 'books', 'course', 'certificate', 'english', 'lesson']
key_health = ['health', 'hygiene', 'pharmacy', 'vitamins', 'doc', 'doctor']
key_transport = ['bus', 'trolleybus', 'tram', 'train', 'plane', 'aircraft', 'airplane', 'taxi']
key_clothing = ['clothing', 'clothes', 'wear']
key_way_of_life = ['home', 'trinket']
key_travelling = ['travel', 'journey', 'trip']
keys = [key_income, key_apartment, key_phone, key_nutrition, key_education,
        key_health, key_transport, key_clothing, key_way_of_life, key_travelling]
