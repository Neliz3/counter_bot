import telegram
import os
from dotenv import load_dotenv


# Initialize environment variables
load_dotenv('/home/elizabeth/runner_bot/.env')


# Initialize a bot
bot = telegram.Bot(token=os.getenv("TOKEN"))


# Initialize admin
admin = os.getenv("ADMIN")
