from google_sheets.auth import gc

def set_pocket_value(sheet_id, new_pocket_value):
    worksheet = gc.open_by_key(sheet_id).sheet1
    cell = worksheet.find('Pocket money')
    worksheet.update_cell(row=cell.row, col=(cell.col + 1), value=new_pocket_value)
    msg = f'{new_pocket_value} grn | Pocket money\n'
    return msg


def get_pocket_value(sheet_id):
    worksheet = gc.open_by_key(sheet_id).sheet1
    cell = worksheet.find('Pocket money')
    pocket_cell_value = worksheet.cell(row=cell.row, col=cell.col + 1).value
    return pocket_cell_value
