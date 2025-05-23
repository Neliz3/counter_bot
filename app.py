import asyncio
from config.config import dp, bot, commands
from telegram_bot.handlers.finance_commands import command_router
from telegram_bot.handlers.manage_start import start_router
from database import Base, engine


def init_db():
    Base.metadata.create_all(bind=engine)


async def on_startup():
    init_db()

    await bot.set_my_commands(commands)

    dp.include_routers(start_router, command_router)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(on_startup())


# TODO: add setup of today statistic
# TODO: add category setup for user
# TODO: add week/month statistic
# TODO: add income table
# TODO: add localization
# TODO: add docker
# TODO: add tests ??
# TODO: add alembic for migrations
