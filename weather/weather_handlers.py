from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import weather.func
from bot import dp
from states import MainState
from keyboards import keyboards


class WeatherState(StatesGroup):
    choise_day = State()

@dp.message_handler(state=MainState.weather_state)
async def choise_day(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await WeatherState.choise_day.set()
    await message.answer('На когда смотрим погоду?', reply_markup=keyboards['weather_day'])

@dp.callback_query_handler(state=WeatherState.choise_day)
async def to_go(call: types.CallbackQuery, state: FSMContext):
    day = int(call.data)
    data = await state.get_data()

    try:
        lon, lat = weather.func.find_city(data['city'])
        weather_data = weather.func.get_data(lon, lat, day)
        await call.message.answer(f'В {data["city"]} {call.message.text} {weather_data["description"]}.')
        await call.message.answer(f'Облачность {weather_data["clouds"]}%.')
        await call.message.answer(f'Утром {weather_data["temp_morn"]}({weather_data["feels_like_morn"]})°C Днём'
                             f' {weather_data["temp_day"]}({weather_data["feels_like_day"]})°C Вечером  '
                             f'{weather_data["temp_eve"]}({weather_data["feels_like_eve"]})°C Ночью  '
                             f'{weather_data["temp_night"]}({weather_data["feels_like_night"]})°C')
        await call.message.answer('Введите название города')
        await MainState.weather_state.set()

    except:
        await call.message.answer('Город не найден')
        await MainState.weather_state.set()
    await call.answer('')

