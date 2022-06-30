import asyncio
from config import bot


async def main():
    print(await bot.get_me())


if __name__ == '__main__':
    asyncio.run(main())
