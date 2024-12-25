from database.db import database as db, Database
from google_sheets.auth import create_copy


async def user_connect(user_id):
    if not await Database().is_exist_user(db, user_id):
        spreadsheet_id = await create_copy()
        await Database().add_user(db, user_id, spreadsheet_id.id)
