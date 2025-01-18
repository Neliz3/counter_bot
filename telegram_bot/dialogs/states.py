from aiogram.fsm.state import State, StatesGroup


class SGMain(StatesGroup):
    trainings = State()


class SGSetup(StatesGroup):
    change_categories = State()


class SGCashFlow(StatesGroup):
    cash_flow = State()
    error_cash_flow = State()


class SGEmail(StatesGroup):
    email = State()
