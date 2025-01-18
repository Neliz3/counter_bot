from types import NoneType

from google_sheets.auth import get_worksheet
from telegram_bot.config import get_message
from google_sheets.auth import logger_sheets


async def update_value(sheet_id, category, value):
    worksheet = await get_worksheet(sheet_id)
    cell = await worksheet.find(category.capitalize())
    value = float(value)

    if cell is None:
        error_msg = await get_message("cash_flow.error")
        raise ValueError(error_msg)
    else:
        existing_value = await worksheet.cell(cell.row, cell.col + 1)
        # logger_sheets.warning(f"Value from cell: {existing_value.value}")
        existing_value = float(existing_value.value) if existing_value and not NoneType else 0
        value += existing_value

        await worksheet.update_cell(row=cell.row, col=(cell.col + 1), value=value)


async def update_category(sheet_id, category, new_title):
    worksheet = await get_worksheet(sheet_id)
    cell = await worksheet.find(category.upper())
    await worksheet.update(new_title, cell)


async def get_value(sheet_id, sheet_name, cell):
    worksheet = await get_worksheet(sheet_id, sheet_name)
    value = await worksheet.acell(cell)
    return value.value


async def set_pocket_value(sheet_id, new_pocket_value):
    worksheet = await get_worksheet(sheet_id)
    cell = await worksheet.find('Pocket money')
    await worksheet.update_cell(row=cell.row, col=(cell.col + 1), value=new_pocket_value)
    msg = f'{new_pocket_value} grn | Pocket money\n'
    return msg


async def get_pocket_value(sheet_id):
    worksheet = await get_worksheet(sheet_id)
    cell = await worksheet.find('Pocket money')
    pocket_cell = await worksheet.cell(row=cell.row, col=cell.col + 1)
    return pocket_cell.value


async def get_expenses_value(sheet_id):
    worksheet = await get_worksheet(sheet_id)
    cell = await worksheet.find('General expenses')
    expenses_cell = await worksheet.cell(row=cell.row, col=cell.col + 1)
    return expenses_cell.value


async def get_range_values(worksheet, cell_range):
    """
    Retrieve values from a specified range in a worksheet [list[list]].
    :param worksheet: The AsyncioGspreadWorksheet object.
    :param cell_range: The range string (e.g., 'A1:C3').
    """
    return await worksheet.get_values(cell_range)


async def get_categories(sheet_id, pretty: bool = False):
    """
    Retrieve sub categories from a specified category.
    :param sheet_id: The AsyncioGspreadWorksheet object.
    :param pretty: Return formatted output for sending a message.
    """
    worksheet = await get_worksheet(sheet_id)
    income = await get_range_values(worksheet, 'A2:A18')
    monthly_payments = await get_range_values(worksheet, 'C2:C18')
    other_expenses = await get_range_values(worksheet, 'E2:E18')

    if not pretty:
        yield income, monthly_payments, other_expenses
    else:
        income_message = await get_message(
            key="categories.cat_income",
            cat="\n".join(f"- {item[0]}" for item in income)
        )
        yield income_message

        monthly_payments_message = await get_message(
            key="categories.cat_monthly_payments",
            cat="\n".join(f"- {item[0]}" for item in monthly_payments)
        )
        yield monthly_payments_message

        other_expenses_message = await get_message(
            key="categories.cat_other_expenses",
            cat="\n".join(f"- {item[0]}" for item in other_expenses)
        )
        yield other_expenses_message
