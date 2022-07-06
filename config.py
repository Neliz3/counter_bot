from telegram.ext import ApplicationBuilder
import os
from dotenv import load_dotenv


# Initialize environment variables
load_dotenv('/home/elizabeth/runner_bot/.env')


# Initialize a bot
application = ApplicationBuilder().token(os.getenv("TOKEN")).build()


# Initialize admin
admin = os.getenv("ADMIN")
