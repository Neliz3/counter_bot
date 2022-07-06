from telegram.ext import filters


only_message = filters.TEXT & (~filters.COMMAND)
