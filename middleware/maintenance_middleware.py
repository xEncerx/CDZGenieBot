from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery, Message, InlineQuery
from config.database.data import Database
from config.bot_data import admin_id
import os

file_path = os.path.join(os.getcwd(), "config", "database", "data.db")

db = Database(file_path)

class MaintenanceMiddleware(BaseMiddleware):
    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        if call.from_user.id not in admin_id:
            if db.get_maintenance_data():
                await call.answer("😔 Технический перерыв 😔\nДаже бот становиться лучше 🧐", show_alert=True)
                raise CancelHandler

    async def on_process_message(self, message: Message, data: dict):
        if message.from_user.id not in admin_id:
            if db.get_maintenance_data():
                await message.answer("<b>😔 Технический перерыв 😔\nДаже бот становиться лучше</b> 🧐")
                raise CancelHandler

    async def on_process_inline_query(self, query: InlineQuery, data: dict):
        if query.from_user.id not in admin_id:
            if db.get_maintenance_data():
                await query.answer("😔 Технический перерыв 😔\nДаже бот становиться лучше 🧐")
                raise CancelHandler



