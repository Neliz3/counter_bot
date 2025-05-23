import yaml
import aiofiles


async def load_messages():
    async with aiofiles.open("telegram_bot/messages.yml", "r") as file:
        content = await file.read()
    return yaml.safe_load(content)


async def get_message(key, **kwargs):
    messages = await load_messages()

    # Split the key by '.' to allow nested key access
    keys = key.split('.')
    message_template = messages["messages"]

    # Traverse through the keys to access nested dictionaries
    for k in keys:
        message_template = message_template.get(k, "Message not found.")

    return message_template.format(**kwargs)


async def load_category_samples() -> dict[str, str]:
    async with aiofiles.open("telegram_bot/ai_cat_detection/category_samples.yml", "r") as file:
        content = await file.read()
    return yaml.safe_load(content)
