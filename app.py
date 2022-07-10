from config import config
import logging
from telegram_bot.handlers.commands import list_handlers
#from server.heroku_server import launch_server
from flask import Flask, request
import telebot


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


@config.bot.message_handler(commands=['start'])
def start(message):
    config.bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


server = Flask(__name__)


@server.route('/' + config.token_bot, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    config.bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    config.bot.remove_webhook()
    config.bot.set_webhook(url=config.app_url)
    return '!', 200


def launch_server():
    server.run(host='0.0.0.0', port=config.port)


def main():
    config.application.add_handlers(list_handlers())
    launch_server()


if __name__ == '__main__':
    main()
