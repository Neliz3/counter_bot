from aiogram.fsm.state import State, StatesGroup


class SGMain(StatesGroup):
    start = State()
    example = State()
    change_categories = State()

class SGFlow(StatesGroup):
    cash_flow = State()

class SGEmail(StatesGroup):
    email = State()
