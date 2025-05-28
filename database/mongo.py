import yaml
import aiofiles
import os
from config.config import logger
from . import categories_collection


CATEGORIES_FOLDER = "telegram_bot/locales/default_categories"


async def add_category_group(user_id: int, group_name: str, items: list[str]):
    await categories_collection.update_one(
        {"_id": str(user_id)},
        {"$set": {f"categories.{group_name}": items}},
        upsert=True
    )


async def delete_category_group(user_id: int, group_name: str) -> bool:
    try:
        await categories_collection.update_one(
            {"_id": str(user_id)},
            {"$unset": {f"categories.{group_name}": ""}}
        )
        return True
    except Exception as e:
        logger.error(f"Exception in delete_category_group: {e}")
        return False


async def get_user_category_samples(user_id: int) -> dict[str, str]:
    doc = await categories_collection.find_one({"_id": str(user_id)})

    if not doc or "categories" not in doc:
        return {}

    return doc["categories"]


async def get_category_names(user_id: int) -> list[str]:
    category_samples = await get_user_category_samples(user_id)
    return list(category_samples.keys())


async def get_category_values(user_id: int) -> list[str]:
    category_samples = await get_user_category_samples(user_id)
    return list(category_samples.values())


async def upload_default_categories():
    for filename in os.listdir(CATEGORIES_FOLDER):
        if filename.startswith("category_") and filename.endswith(".yml"):
            parts = filename.removeprefix("category_").removesuffix(".yml")
            language = parts.strip()
            key = f"default_{language}"
            filepath = os.path.join(CATEGORIES_FOLDER, filename)

            async with aiofiles.open(filepath, "r", encoding="utf-8") as file:
                content = await file.read()
                categories = yaml.safe_load(content)

            await categories_collection.update_one(
                {"_id": key},
                {"$set": {"categories": categories}},
                upsert=True
            )


async def initialize_user_categories(user_id: int, lang: str = "uk"):
    default_doc = await categories_collection.find_one({"_id": f"default_{lang}"})
    if not default_doc:
        raise Exception("Default categories not uploaded yet")

    exists = await categories_collection.find_one({"_id": str(user_id)})
    if not exists:
        await categories_collection.insert_one({
            "_id": str(user_id),
            "categories": default_doc["categories"]
        })
