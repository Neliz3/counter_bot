from telegram.ext import filters


only_message = filters.ALL & (~filters.COMMAND)

# TODO setting a filter that will search a link using key words in url