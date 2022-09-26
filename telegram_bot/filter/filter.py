from telegram.ext import filters


# Filter is used for finding messages with numbers
only_message = filters.TEXT & (~filters.COMMAND)

# TODO setting a filter that will search a link using key words in url
# TODO a url or an url
