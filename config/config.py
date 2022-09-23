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
