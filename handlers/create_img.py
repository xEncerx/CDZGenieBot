from aiogram import types, Dispatcher
from config.bot_data import bot
import markups as nav
from utils.message_utils import text_editor
from markups import cb
from aiogram.dispatcher import FSMContext
from states.CDZParam import CDZParam
from middleware.throttling_middleware import rate_limit
import asyncio
from utils.generate_img import aio_create_img

async def main_commands(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    if action == "change_name":
        await text_editor(text="Введите имя, которое будет отображаться в ЦДЗ\n"
                               "<b>Формат:</b> <code>Имя Фамилия</code>", call=call, markup=nav.back_button("creation"))
        await CDZParam.get_client_name.set()
    if action == "CDZ_name":
        await text_editor(text="Введите название ЦДЗ", call=call, markup=nav.back_button("creation"))
        await CDZParam.get_CDZ_name.set()
    if action == "windows":
        await text_editor(text=f"Изображение будет создано под систему <b>{action}</b>", call=call, markup=nav.create_img_keyboard({'windows': 1, 'android': 0, 'iphone': 0}))
        await state.update_data(system={'windows': 1, 'android': 0, 'iphone': 0})
    if action == "android":
        await text_editor(text=f"Изображение будет создано под систему <b>{action}</b>", call=call,
                          markup=nav.create_img_keyboard({'windows': 0, 'android': 1, 'iphone': 0}))
        await state.update_data(system={'windows': 0, 'android': 1, 'iphone': 0})
    if action == "iphone":
        await text_editor(text=f"Изображение будет создано под систему <b>{action}</b>", call=call,
                          markup=nav.create_img_keyboard({'windows': 0, 'android': 0, 'iphone': 1}))
        await state.update_data(system={'windows': 0, 'android': 0, 'iphone': 1})
    if action == "extra_param":
        await text_editor(text=f"<b>Данные параметры указывать необязательно, чтобы создать изображение!</b>\n\n"
                               f"<i>• Время - будет указано текущее время, но вы можете указать любое</i>\n"
                               f"<i>• Кол-во заданий - кол-во правильных|неправильных заданий</i>\n"
                               f"<i>• Text Wrap - кол-во символов на 1 строке(изменять если текст залезает за рамки экрана)</i>", call=call, markup=nav.extra_menu)
    if action == "change_time":
        await text_editor(text="Укажите время.\n<b>Формат:</b> <code>Часы:Минуты</code>", call=call, markup=nav.back_button("creation"))
        await CDZParam.get_time.set()
    if action == "change_number":
        await call.answer("⚠️ Данный параметр находиться в beta тесте ⚠️", show_alert=True)
        await text_editor(text="Укажите кол-во правильных|неправильных заданий\n"
                               "<b>Формат 1:</b> <i>1 число - правильные</i>\n"
                               "<b>Формат 2 :</b> <i>2 числа(12 2) - правильные неправильные</i>", call=call, markup=nav.back_button("creation"))
        await CDZParam.get_number.set()
    if action == "change_text_wrap":
        await call.answer("⚠️ Рекомендуется не изменять данный параметр ⚠️", show_alert=False)
        await text_editor(text="<b>Укажите кол-во символов на 1 строке.</b>\n"
                               "<b>По умолчанию:</b> <i>Android:</i> <code>47</code>, <i>Iphone:</i> <code>55</code>",
                          call=call, markup=nav.back_button("creation"))
        await CDZParam.get_text_wrap.set()
    await call.answer()

async def update_data(state: FSMContext):
    async with state.proxy() as data:
        system = data.get("system", {'windows': 1, 'android': 0, 'iphone': 0})
        cdz_name = data.get("cdz_name")
        time = data.get("time")
        answer = data.get("answer")
        client_name = data.get("client_name")
        text_wrap = data.get("text_wrap")
    await state.finish()
    await CDZParam.start.set()
    await state.update_data(client_name=client_name, system=system, cdz_name=cdz_name, time=time, answer=answer, text_wrap=text_wrap)


async def get_text_wrap(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text_wrap"] = message.text
        system = data.get("system", {'windows': 1, 'android': 0, 'iphone': 0})
    if len(data["text_wrap"].split()) == 1 and data["text_wrap"].isdigit():
        await text_editor(text=f"🎉 Кол-во символов в строке успешно изменено на <b>{data['text_wrap']}</b>", message=message,
                          markup=nav.create_img_keyboard(system), is_call=False)
        await state.update_data(text_wrap=data["text_wrap"])
    else:
        await text_editor(text="❌ <b>Неверный формат данных</b>", message=message,
                          markup=nav.create_img_keyboard(system), is_call=False)
    await update_data(state=state)

async def get_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer"] = message.text.split()
        system = data.get("system", {'windows': 1, 'android': 0, 'iphone': 0})
        answer = list(data["answer"])
    if len(answer) == 1: answer.append("0")
    if all(map(str.isdigit, answer)):
        await text_editor(text=f"🎉 Кол-во заданий успешно изменено на <b>{' '.join(answer)}</b>",
                          message=message,
                          markup=nav.create_img_keyboard(system), is_call=False)
    else:
        answer = None
        await text_editor(text="❌ <b>Неверный формат данных</b>", message=message, markup=nav.create_img_keyboard(system), is_call=False)
    async with state.proxy() as data:
        data["answer"] = answer
    await update_data(state=state)

async def get_client_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["client_name"] = message.text
        system = data.get("system", {'windows': 1, 'android': 0, 'iphone': 0})
    await text_editor(text=f"🎉 Имя успешно изменено на <b>{data['client_name']}</b>", message=message, markup=nav.create_img_keyboard(system), is_call=False)
    await state.update_data(client_name=data["client_name"])
    await update_data(state=state)

async def get_cdz_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["cdz_name"] = message.text
        system = data.get("system", {'windows': 1, 'android': 0, 'iphone': 0})
    await text_editor(text=f"🎉 Название ЦДЗ успешно изменено на <b>{data['cdz_name']}</b>", message=message, markup=nav.create_img_keyboard(system), is_call=False)
    await state.update_data(cdz_name=data["cdz_name"])
    await update_data(state=state)

async def get_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["time"] = message.text
        system = data.get("system", {'windows': 1, 'android': 0, 'iphone': 0})
    await text_editor(text=f"🎉 Время успешно изменено на <b>{data['time']}</b>", message=message, markup=nav.create_img_keyboard(system), is_call=False)
    await state.update_data(time=data["time"])
    await update_data(state=state)

@rate_limit(20, key="create_img")
async def create_img(call: types.CallbackQuery, state: FSMContext):
    await text_editor("🖨 Идет создание изображения...", call=call)
    async with state.proxy() as data:
        client_name = data.get("client_name")
        system_dict = data.get("system")
        cdz_name = data.get("cdz_name")
        time = data.get("time")
        answer = data.get("answer")
        text_wrap = data.get("text_wrap")
        if client_name and system_dict and cdz_name:
            system = next(key for key, value in data.get("system").items() if value == 1)
            asyncio.create_task(aio_create_img(call.from_user.id, cdz_name=cdz_name, client_name=client_name, time=time, answer=answer, system=system, text_wrap=text_wrap))
        else:
            await bot.send_message(call.from_user.id, "❗️ Создание изображения отменено. Не все основные параметры были указаны ❗️", reply_markup=nav.main_menu)
    await state.finish()
    await call.answer()


def register_handlers_create_img(dp: Dispatcher):
    dp.register_callback_query_handler(main_commands, cb.filter(action=["extra_param", "CDZ_name", "change_name", "change_number",
                                                                        "iphone", "android", "windows", "change_time", "change_text_wrap"]), state=CDZParam.start)
    dp.register_message_handler(get_cdz_name, state=CDZParam.get_CDZ_name)
    dp.register_message_handler(get_client_name, state=CDZParam.get_client_name)
    dp.register_message_handler(get_time, state=CDZParam.get_time)
    dp.register_message_handler(get_answer, state=CDZParam.get_number)
    dp.register_message_handler(get_text_wrap, state=CDZParam.get_text_wrap)
    dp.register_callback_query_handler(create_img, cb.filter(action=["create_img"]), state="*")