from flask import Flask, request
from telegram_bot.config import config


server = Flask(__name__)


@server.route('/' + config.token_bot, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = config.application.types.Update.de_json(json_string)
    config.application.process_update([update])
    #config.application.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    config.application.bot.delete_webhook()
    config.application.bot.set_webhook(url=config.app_url)
    return '!', 200


def launch_server():
    server.run(host='0.0.0.0', port=config.port)
