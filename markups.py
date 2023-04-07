from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cb = CallbackData("fabnum", "action")

main_menu = InlineKeyboardMarkup(row_width=1)
main_menu.add(InlineKeyboardButton("🔧 Создать изображение", callback_data=cb.new("creation_menu")))

extra_menu = InlineKeyboardMarkup(row_width=1)
extra_menu.add(InlineKeyboardButton("⏰ Изменить время", callback_data=cb.new(action="change_time")),
               InlineKeyboardButton("📝 Кол-во заданий", callback_data=cb.new(action="change_number")),
               InlineKeyboardButton("📃 Text Wrap", callback_data=cb.new(action="change_text_wrap")),
               InlineKeyboardButton("🔙 Назад", callback_data=cb.new(action="back|creation")))

def create_img_keyboard(system_dict: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.row(InlineKeyboardButton("👤 Изменить имя", callback_data=cb.new(action="change_name")),
                 InlineKeyboardButton("🖋 Название ЦДЗ", callback_data=cb.new(action="CDZ_name")))
    keyboard.row()
    for system, value in system_dict.items():
        keyboard.insert(InlineKeyboardButton(f"{system} {'✅' if bool(value) else '❌'}", callback_data=cb.new(action=system)))
    keyboard.add(InlineKeyboardButton("📃 Доп. Параметры", callback_data=cb.new(action="extra_param")))
    keyboard.add(InlineKeyboardButton("🖨 Создать изображение", callback_data=cb.new(action="create_img")))
    keyboard.add(InlineKeyboardButton("🔙 Отмена", callback_data=cb.new(action="back|main")))
    return keyboard


def back_button(data: str, text: str = "🔙 Назад") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text, callback_data=cb.new(action=f"back|{data}")))
    return keyboard