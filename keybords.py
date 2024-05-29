from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def generate_save_city_keyboard(city_name: str) -> InlineKeyboardMarkup:
    """
    Generates and returns keyboard with one button to save city name
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Shaharni saqlash", callback_data=f"{city_name}")]
    ])

    return keyboard


def generate_cities_menu(cities_list: list) -> ReplyKeyboardMarkup:
    """
    Generates and returs cities list for user
    """
    markup = ReplyKeyboardBuilder()

    for city in cities_list:
        markup.button(text=city.get('city_name').title())
    markup.adjust(2)
    markup.row(KeyboardButton(text= "❌Shaharlar ro'yhatini ochirish"))
    
    return markup.as_markup(resize_keyboard=True)

