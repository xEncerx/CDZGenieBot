from aiogram import types
from config.bot_data import bot
from aiogram.utils.exceptions import MessageNotModified, BadRequest


async def text_editor(text: str, call: types.CallbackQuery = None, markup=None, is_call: bool = True, message: types.Message = None):
    chat_id = call.from_user.id if is_call else message.from_user.id
    message_id = call.message.message_id if is_call else message.message_id
    try:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup,
                                    parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
    except MessageNotModified:
        pass
    except BadRequest:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode=types.ParseMode.HTML,
                               disable_web_page_preview=True)


