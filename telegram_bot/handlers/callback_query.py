from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes


# Answer to a query button
async def query_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    await query.edit_message_text(text=f"❌ Open https://docs.google.com/spreadsheets/d/1C-Z0OPYnyKPSjn8_YvrpE4uFIPiw0xQrSTn2OHhPVO4/edit#gid=1785411570"
                                       f"\n❌ Click 'File' or tree points at the top\n"
                                       f"❌ Click 'Share and export' and 'Make a copy'\n"
                                       f"❌ Click 'Share and export' again\n"
                                       f"❌ Click 'Share access' for editing with\n"
                                       f"❌ `telegram-bot-service@counter-bot-361806.iam.gserviceaccount.com`\n"
                                       f"❌ Copy URL of a page and send it to me!"
                                  )


def list_query():
    start_handler = CallbackQueryHandler(query_start)
    return start_handler
