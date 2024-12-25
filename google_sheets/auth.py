import gspread_asyncio
from google.oauth2.service_account import Credentials
from datetime import datetime
import gspread


def get_creds():
    """
    Returns a Credentials object.
    """
    creds = Credentials.from_service_account_file("service_account.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


agc_manager = gspread_asyncio.AsyncioGspreadClientManager(get_creds)
gs = gspread.authorize(get_creds())


async def get_spreadsheet(spreadsheet_id=None, spreadsheet_name=None):
    """
    Returns a Google Sheet spreadsheet using the ID.
    """
    agc = await agc_manager.authorize()
    if spreadsheet_name:
        return await agc.open(spreadsheet_name)
    else:
        return await agc.open_by_key(spreadsheet_id)


async def get_worksheet_name() -> str:
    """
    Returns the worksheet name using month and year.
    """
    month = datetime.now().strftime("%b")
    year = datetime.now().strftime("%y")
    worksheet_name = f"{month} {year}"
    return worksheet_name


async def get_worksheet(spreadsheet_id, sheet_name=None):
    """
    Returns a Google Sheet worksheet using spreadsheet ID and sheet name.
    """
    spreadsheet = await get_spreadsheet(spreadsheet_id=spreadsheet_id)
    if sheet_name:
        return await spreadsheet.worksheet(sheet_name)
    else:
        worksheet_name = await get_worksheet_name()
        return await spreadsheet.worksheet(worksheet_name)


async def update_worksheet_title_sync(spreadsheet_id, new_title):
    """
    Updates the worksheet title using gspread synchronous library in an async context.
    """
    sync_spreadsheet = gs.open_by_key(spreadsheet_id)
    worksheet = sync_spreadsheet.get_worksheet(0)
    worksheet.update_title(new_title)


async def create_copy():
    """
    Returns a Google Sheet spreadsheet copy of Template worksheet.
    """
    agc = await agc_manager.authorize()
    template_title = "Template expenses per month"
    template_spreadsheet = await get_spreadsheet(
        spreadsheet_name=template_title)

    copy_title = "Money Expenses"
    copied_spreadsheet = await agc.copy(
        template_spreadsheet.id, title=copy_title)

    # Rename the worksheet using today's date
    worksheet_name = await get_worksheet_name()
    await update_worksheet_title_sync(copied_spreadsheet.id, worksheet_name)

    return copied_spreadsheet


def share_access_sync(user_email, sheet_id) -> str:
    """
    Shares access for a Google Sheet spreadsheet to a user using sync gspread library.
    """
    try:
        sync_spreadsheet = gs.open_by_key(sheet_id)
        sync_spreadsheet.share(user_email, perm_type='user', role='writer')

        sms = (f"Shared the spreadsheet with {user_email} successfully!\n"
               f"To open, click {sync_spreadsheet.url}")
    except Exception as e:
        sms = f"Write correct email address. Error: {e}"
    return sms
