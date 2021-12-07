from aiogram import types
from aiogram.dispatcher import FSMContext
import weather.func
from bot import bot, dp, MainState
from keyboards import keyboards




@dp.message_handler(state=MainState.weather_state)
async def choise_day(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await MainState.weather_state_day.set()
    await message.answer('На когда смотрим погоду?', reply_markup=keyboards['weather_day'])


@dp.callback_query_handler(state=[MainState.weather_state_day, MainState.weather_state])
async def to_go(call: types.CallbackQuery, state: FSMContext):
    day_text = {0: 'Сегодня', 1: 'Завтра', 2: 'Послезавтра'}

    day = int(call.data)
    data = await state.get_data()

    try:
        lon, lat = weather.func.find_city(data['city'])
        weather_data = weather.func.get_data(lon, lat, day)
        await bot.send_photo(chat_id=call.message.chat.id, photo=weather_data["url_ico"])
        await call.message.answer(
            f'В городе {data["city"]}, {day_text[day].lower()} - {weather_data["description"]}.')
        await call.message.answer(f'Облачность {weather_data["clouds"]}%.')
        await call.message.answer(f'Утром {weather_data["temp_morn"]}°C, Ощущается как {weather_data["feels_like_morn"]}°C\n'
                                  f'Днём {weather_data["temp_day"]}°C, Ощущается как {weather_data["feels_like_day"]}°C\n'
                                  f'Вечером {weather_data["temp_eve"]}°C, Ощущается как {weather_data["feels_like_eve"]}°C\n'
                                  f'Ночью {weather_data["temp_night"]}°C, Ощущается как {weather_data["feels_like_night"]}°C')
        await call.message.answer('Посмотрим в другом городе?')
        await MainState.weather_state.set()

    except:
        await call.message.answer('Город не найден')
        await MainState.weather_state.set()
    await call.answer('')

