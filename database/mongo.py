import yaml
import aiofiles
from . import categories_collection
from config.config import logger


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
    async with aiofiles.open("telegram_bot/default_categories.yml", "r", encoding="utf-8") as file:
        content = await file.read()

        default_data = yaml.safe_load(content)

    await categories_collection.update_one(
        {"_id": "default"},
        {"$set": {"categories": default_data}},
        upsert=True
    )



async def initialize_user_categories(user_id: int):
    default_doc = await categories_collection.find_one({"_id": "default"})
    if not default_doc:
        raise Exception("Default categories not uploaded yet")

    exists = await categories_collection.find_one({"_id": str(user_id)})
    if not exists:
        await categories_collection.insert_one({
            "_id": str(user_id),
            "categories": default_doc["categories"]
        })
