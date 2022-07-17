from aiogram.dispatcher.filters.state import StatesGroup, State

class RegisterState(StatesGroup):
    name = State()
    phone = State()
    email = State()

class UpdateDataState(StatesGroup):
    name = State()
    phone = State()
    email = State()

class OrderState(StatesGroup):
    order = State()
    order_msg = State()
    myorders = State()

class ContactState(StatesGroup):
    reply_msg = State()
    contact = State()

