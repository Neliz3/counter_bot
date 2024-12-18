import gspread


# Authenticate using the service account credentials
gc = gspread.service_account(
    scopes=["https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"]
)

def create_copy() -> gspread.Spreadsheet:
    template_sheet = gc.open("Template expenses per month")

    copy_title = "Money Expenses"
    copied_sheet = gc.copy(template_sheet.id, title=copy_title)
    return copied_sheet


def share_access(user_email, sheet_id) -> str:
    user_sheet = gc.open_by_key(sheet_id)

    try:
        user_sheet.share(user_email, perm_type='user', role='writer')
        sms = (f"Shared the spreadsheet with {user_email} successfully!\n"
               f"To open, click {user_sheet.url}")
    except Exception as e:
        sms = f"Write correct email address. Error: {e}"
    return sms
