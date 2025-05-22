import asyncio
from config.config import dp, bot, commands
from telegram_bot.handlers.commands import command_router
from database import Base, engine


def init_db():
    Base.metadata.create_all(bind=engine)


async def on_startup():
    init_db()

    await bot.set_my_commands(commands)

    dp.include_router(command_router)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(on_startup())
