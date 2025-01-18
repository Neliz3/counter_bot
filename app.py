from aiogram_dialog import setup_dialogs
from config.config import dp, bot, commands
from telegram_bot.handlers.commands import router
import asyncio
from database.db import database
from telegram_bot.dialogs.counter_dialogs import main_dialog, email_dialog, cash_flow_dialog


async def on_startup():
    await bot.set_my_commands(commands)

    dp.include_router(router)
    dp.include_routers(main_dialog, email_dialog, cash_flow_dialog)
    setup_dialogs(dp)

    await dp.start_polling(bot, skip_updates=True)


async def on_shutdown():
    await database.close()


if __name__ == '__main__':
    asyncio.run(on_startup())
    asyncio.run(on_shutdown())
