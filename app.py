import asyncio
from config.config import commands, get_bot, get_dp
from telegram_bot.handlers import (
    manage_start as ms, statistics as st, user_input_handling as ui, categories as ct
)
from database import Base, engine
from database.mongo import upload_default_categories
from telegram_bot.filters.text_i18n import TextI18nFilter


async def init_db():
    Base.metadata.create_all(bind=engine)
    await upload_default_categories()


async def on_startup():
    bot = get_bot()
    dp = get_dp()

    await init_db()

    await bot.set_my_commands(commands)

    dp.message.filter(TextI18nFilter)
    dp.include_routers(ms.start_router, st.statistics_router, ct.cat_router, ui.user_input_router)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(on_startup())
