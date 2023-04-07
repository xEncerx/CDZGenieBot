import aiogram.types
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# ___________________________________________________________________
admin_id = [1011107842]
token = "6093680010:AAG54K94-tz7azwpqvHAxnOw2RYxNaU8YBQ"
admin_chat = "xEncerx"
# ___________________________________________________________________
bot = Bot(token=token, parse_mode=aiogram.types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

