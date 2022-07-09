from telegram.ext import ApplicationBuilder
import os
from dotenv import load_dotenv


# Initialize environment variables
load_dotenv('/home/elizabeth/counter_bot/telegram_bot/config/.env')


# Initialize a bot
token_bot = os.getenv("TOKEN")
application = ApplicationBuilder().token(token_bot).build()


# Initialize admin
admin = os.getenv("ADMIN")


# Initialize app on Heroku server
app_url = os.getenv("APP_URL") + token_bot
port = int(os.environ.get('PORT', 5000))
