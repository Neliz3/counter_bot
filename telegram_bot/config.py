# import yaml
#
#
# # Load messages from the YAML file
# with open("telegram_bot/messages.yml", "r") as file:
#     messages = yaml.safe_load(file)
#
# # Access and dynamically fill a message
# def get_message(key, **kwargs):
#     """
#     Retrieve a message by key and dynamically insert variables.
#     """
#     message_template = messages["messages"].get(key, "Message not found.")
#     return message_template.format(**kwargs)


import yaml
import aiofiles


async def load_messages():
    async with aiofiles.open("telegram_bot/messages.yml", "r") as file:
        content = await file.read()
    return yaml.safe_load(content)


# async def get_message(key, **kwargs):
#     messages = await load_messages()
#     message_template = messages["messages"].get(key, "Message not found.")
#     return message_template.format(**kwargs)


async def get_message(key, **kwargs):
    messages = await load_messages()

    # Split the key by '.' to allow nested key access
    keys = key.split('.')
    message_template = messages["messages"]

    # Traverse through the keys to access nested dictionaries
    for k in keys:
        message_template = message_template.get(k, "Message not found.")

    return message_template.format(**kwargs)
