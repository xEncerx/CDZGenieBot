from aiogram.dispatcher.filters.state import StatesGroup, State

class CDZParam(StatesGroup):
    start = State()
    get_client_name = State()
    get_time = State()
    get_number = State()
    get_CDZ_name = State()
    get_text_wrap = State()