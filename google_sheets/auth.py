import gspread_asyncio
from google.oauth2.service_account import Credentials
from datetime import datetime
import gspread
import logging


logger_sheets = logging.getLogger("GoogleSheets")


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


async def clear_range_in_worksheet(sheet_id, worksheet_title, cell_range):
    """
    Clears the content of a specified range of cells in a worksheet.
    """
    spreadsheet = await get_spreadsheet(sheet_id)
    worksheet = await spreadsheet.worksheet(worksheet_title)

    cell_list = await worksheet.range(cell_range)
    for cell in cell_list:
        cell.value = ""
    await worksheet.update_cells(cell_list)


async def new_worksheet_sync(sheet_id):
    """
    Creates a new worksheet using gspread synchronous library.
    """
    sync_spreadsheet = gs.open_by_key(sheet_id)
    last_worksheet_template = sync_spreadsheet.get_worksheet(0)

    new_title = await get_worksheet_name()
    new_month_worksheet = last_worksheet_template.duplicate(
        new_sheet_name=new_title, insert_sheet_index=0)

    await clear_range_in_worksheet(sync_spreadsheet.id, new_title, "B2:B18")
    await clear_range_in_worksheet(sync_spreadsheet.id, new_title, "D2:D18")
    await clear_range_in_worksheet(sync_spreadsheet.id, new_title, "F2:F18")
    return new_month_worksheet


async def get_worksheet(spreadsheet_id, sheet_name=None):
    """
    Returns a Google Sheet worksheet using spreadsheet ID and sheet name.
    """
    spreadsheet = await get_spreadsheet(spreadsheet_id=spreadsheet_id)
    if sheet_name:
        return await spreadsheet.worksheet(sheet_name)
    else:
        worksheet_name = await get_worksheet_name()
        # Handle the change of time and name of the worksheet
        try:
            return await spreadsheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            return await new_worksheet_sync(spreadsheet_id)


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
