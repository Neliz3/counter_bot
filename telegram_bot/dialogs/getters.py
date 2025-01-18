from aiogram_dialog import DialogManager


async def get_trainings(dialog_manager: DialogManager, **kwargs):
    return {
        "trainings": dialog_manager.find("trainings").get_value(),
    }

async def get_cash_flow(dialog_manager: DialogManager, **kwargs):
    return {
        "cash_flow": dialog_manager.find("cash_flow").get_value(),
    }

async def get_email(dialog_manager: DialogManager, **kwargs):
    return {
        "email": dialog_manager.find("email").get_value(),
    }
