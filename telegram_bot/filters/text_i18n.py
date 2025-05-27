from aiogram.filters import BaseFilter
from aiogram.types import Message
from telegram_bot.handlers.manage_start import i18n


class TextI18nFilter(BaseFilter):
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        expected_text = await i18n.get(key=self.key, user_id=user_id)
        return message.text == expected_text
