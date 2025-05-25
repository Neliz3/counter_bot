from aiogram.fsm.state import State, StatesGroup


class CategoryDialog(StatesGroup):
    ChoosingAction = State()
    Adding = State()
    ConfirmAdd = State()
    AddingKeywords = State()  # NEW
    DeletingChoose = State()
    ConfirmDelete = State()
