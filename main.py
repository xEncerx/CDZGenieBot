from aiogram import executor, Dispatcher
from handlers import client, create_img
from middleware import setup_middleware
from config.bot_data import dp, bot
from utils.bot_logging import logging

async def on_startup(dp: Dispatcher):
    me = await bot.get_me()
    logging.critical(f"{me.first_name} [@{me.username}] STARTED")
    setup_middleware(dp)

client.register_handlers_client(dp)
create_img.register_handlers_create_img(dp)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
