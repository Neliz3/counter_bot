from config.config import dp, bot, commands
from telegram_bot.handlers.commands import router
import asyncio
from database.db import database
from telegram_bot.dialogs import register_dialogs


async def on_startup():
    await bot.set_my_commands(commands)

    dp.include_router(router)
    await register_dialogs(dp)

    await dp.start_polling(bot, skip_updates=True)


async def on_shutdown():
    await database.close()


if __name__ == '__main__':
    asyncio.run(on_startup())
    asyncio.run(on_shutdown())


# TODO: implement dialog library
# TODO: add months logic

# setup time
# setup sheet
# today's every time
