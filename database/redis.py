import redis.asyncio as redis
from config.config import DEFAULT_LANG


redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def _key(user_id, name):
    return f"user:{user_id}:{name}"


def _key_lang(user_id, lang):
    return f"user_lang:{user_id}:{lang}"


async def set_temp_income(user_id: int, amount: float):
    await redis_client.set(_key(user_id, "temp_income"), amount, ex=600)


async def get_temp_income(user_id: int) -> float:
    val = await redis_client.get(_key(user_id, "temp_income"))
    return float(val) if val else 0.0


async def set_state(user_id: int, state: str):
    await redis_client.set(_key(user_id, "state"), state, ex=600)


async def get_state(user_id: int) -> str:
    return await redis_client.get(_key(user_id, "state"))


async def clear_state(user_id: int):
    await redis_client.delete(_key(user_id, "state"))


async def set_temp_spending(user_id: int, amount: float):
    await redis_client.set(_key(user_id, "temp_spending"), amount, ex=600)


async def set_temp_desc(user_id: int, desc: str):
    await redis_client.set(_key(user_id, "temp_desc"), desc, ex=600)


async def get_temp_spending(user_id) -> float:
    val = await redis_client.get(_key(user_id, "temp_spending"))
    return float(val) if val else 0.0


async def get_temp_desc(user_id) -> str:
    return await redis_client.get(_key(user_id, "temp_desc"))


async def set_temp_cat(user_id: int, desc: str):
    await redis_client.set(_key(user_id, "temp_cat"), desc, ex=600)


async def get_temp_cat(user_id) -> str:
    return await redis_client.get(_key(user_id, "temp_cat"))


async def get_user_lang(user_id: int) -> str:
    return await redis_client.get(_key_lang(user_id, "lang")) or DEFAULT_LANG


async def set_user_lang(user_id: int, lang: str = DEFAULT_LANG):
    await redis_client.set(_key_lang(user_id, "lang"), lang)


async def clear_user_lang(user_id: int):
    await redis_client.delete(_key_lang(user_id, "lang"))
