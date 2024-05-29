import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from weather import get_weather_data
from database import register_user, register_city, get_user, get_cities, clear_cities_list
from keybords import generate_save_city_keyboard, generate_cities_menu

TOKEN = "1824188034:AAFTl8NWtqN-Hji_sEaUuxDVw6Wgk4NGP_A"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def say_hello(message: Message):
    telegram_id = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username

    try:
        register_user(telegram_id=telegram_id,
                      fullname=fullname, username=username)
        await message.answer(text="Assalomu alaykum !\nMuvaffaqiyatli ro'yxatga olindingiz")
    except:
        await message.answer(text="Xush kelibsiz !\nQaytganingizdan xursandmiz")


@dp.message()
async def send_weather_data(message: Message):

    if message.text.strip() == "❌Shaharlar ro'yhatini ochirish":
        user = get_user(message.from_user.id)
        clear_cities_list(user.get("id"))
        await message.answer(text= "✅Shaharlar ro'yhati tozalandi", reply_markup=ReplyKeyboardRemove())
    
    else:
        weather_data = get_weather_data(city_name=message.text)
        if weather_data:
            await message.answer(
                text=weather_data, 
                reply_markup=generate_save_city_keyboard(city_name=message.text)
            )
        
        else:
            await message.answer(text="Shahar topilmadi")


@dp.callback_query()
async def save_city(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_id = get_user(telegram_id=telegram_id).get('id')
    city_name = call.data

    try:
        register_city(user_id=user_id, city_name=city_name)
    except:
        pass

    cities_list = get_cities(user_id=user_id)
    await call.message.answer(text="Shahar saqlandi ✅", 
                              reply_markup=generate_cities_menu(cities_list=cities_list))
    
    

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
