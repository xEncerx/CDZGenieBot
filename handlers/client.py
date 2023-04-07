from aiogram import types, Dispatcher
from config.bot_data import bot, admin_id
import markups as nav
from utils.message_utils import text_editor
from states.CDZParam import CDZParam
from markups import cb
from aiogram.dispatcher import FSMContext
from middleware.throttling_middleware import rate_limit
from middleware.maintenance_middleware import db
from handlers.create_img import update_data

@rate_limit(2)
async def start(message: types.Message):
    if not db.client_exists(message.from_user.id):
        db.add_client(message.from_user.id)
        await bot.send_message(admin_id[0], f"🎉 Новый пользователь <b>{message.from_user.full_name}</b> - @{message.from_user.username}")
    await bot.send_message(message.from_user.id, f"👋 Привет, <b>{message.from_user.full_name}</b>", reply_markup=nav.main_menu)

async def maintenance(message: types.Message):
    text = message.text.split()[1].lower()
    if text in ["1", "true", "on"]:
        db.update_maintenance_data("1")
        await bot.send_message(message.from_user.id, "❗️ <b>Технический перерыв включён</b> ❗️", reply_markup=nav.main_menu)
    elif text in ["0", "false", "off"]:
        db.update_maintenance_data("0")
        await bot.send_message(message.from_user.id, "❗️ <b>Технический перерыв выключен</b> ❗️",
                               reply_markup=nav.main_menu)

async def back_button(call: types.CallbackQuery, state: FSMContext):
    action = call.data
    action = action[action.find("|")+1:]
    if action == "main":
        if await state.get_state() is not None:
            await state.finish()
        await text_editor(text=f"👋 Привет, <b>{call.from_user.full_name}</b>",
                          call=call,
                          markup=nav.main_menu)
    if action == "creation":
        async with state.proxy() as data:
            system = data.get("system", {'windows': 1, 'android': 0, 'iphone': 0})
            await text_editor(text="Для создания изображения ЦДЗ, заполни необходимые параметры ниже 👇", call=call,
                              markup=nav.create_img_keyboard(system))
        await update_data(state=state)

async def main_commands(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "creation_menu":
        await text_editor(text="Для создания изображения ЦДЗ, заполни необходимые параметры ниже 👇",  call=call, markup=nav.create_img_keyboard({'windows': 1, 'android': 0, 'iphone': 0}))
        await CDZParam.start.set()
    await call.answer()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(maintenance, text_contains="/m", user_id=admin_id, state="*")
    dp.register_callback_query_handler(main_commands, cb.filter(action=["creation_menu"]))
    dp.register_callback_query_handler(back_button, text_contains="back|", state="*")