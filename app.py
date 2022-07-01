import asyncio
from config import bot, admin


async def main():
    async with bot:
        print((await bot.get_updates())[0])
        await bot.send_message(text='Bot started', chat_id=admin)


if __name__ == '__main__':
    asyncio.run(main())
