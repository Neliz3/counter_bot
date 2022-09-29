from telegram.ext import filters


# Filter is used for separation messages and commands
only_message = filters.TEXT & (~filters.COMMAND)
