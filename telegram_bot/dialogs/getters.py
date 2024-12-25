from aiogram_dialog import DialogManager


async def get_example(dialog_manager: DialogManager, **kwargs):
    return {
        "example": dialog_manager.find("example").get_value(),
    }

async def get_cash_flow(dialog_manager: DialogManager, **kwargs):
    return {
        "cash_flow": dialog_manager.find("cash_flow").get_value(),
    }

async def get_email(dialog_manager: DialogManager, **kwargs):
    return {
        "email": dialog_manager.find("email").get_value(),
    }
