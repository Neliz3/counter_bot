from database.db import exist_user, add_user
from google_sheets.auth import create_copy

def user_connect(user_id):
    if not exist_user(user_id):
        sheet_id = create_copy().id
        add_user(user_id, sheet_id)
