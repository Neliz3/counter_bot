import redis.asyncio as redis


redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def _key(user_id, name):
    return f"user:{user_id}:{name}"


async def set_draft_income(user_id: int, amount: float):
    await redis_client.set(_key(user_id, "draft_income"), amount, ex=600)


async def get_draft_income(user_id: int) -> float:
    val = await redis_client.get(_key(user_id, "draft_income"))
    return float(val) if val else 0.0


async def set_state(user_id: int, state: str):
    await redis_client.set(_key(user_id, "state"), state, ex=600)


async def get_state(user_id: int) -> str:
    return await redis_client.get(_key(user_id, "state"))


async def clear_state(user_id: int):
    await redis_client.delete(_key(user_id, "state"))
