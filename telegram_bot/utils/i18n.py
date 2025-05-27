import yaml
import aiofiles
from pathlib import Path
from database.redis import get_user_lang
from config.config import DEFAULT_LANG


MESSAGES_CACHE = {}


class I18n:
    def __init__(self, base_path: str = "telegram_bot/locales", default_lang: str = DEFAULT_LANG):
        self.base_path = Path(base_path)
        self.default_lang = default_lang
        self.cache = {}

    async def load_language(self, lang: str):
        if lang in self.cache:
            return self.cache[lang]

        file_path = self.base_path / f"{lang}.yml"
        if not file_path.exists():
            file_path = self.base_path / f"{self.default_lang}.yml"

        async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
            content = await file.read()
        data = yaml.safe_load(content)
        self.cache[lang] = data
        return data

    async def get(self, key: str, user_id: int, **kwargs) -> str:
        lang = await get_user_lang(user_id)
        data = await self.load_language(lang)
        keys = key.split(".")
        value = data

        for k in keys:
            value = value.get(k)
            if value is None:
                return f"[Missing key: {key}]"

        if isinstance(value, str):
            return value.format(**kwargs)
        return value
