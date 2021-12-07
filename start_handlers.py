from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import keyboards
from bot import bot, dp, MainState
from data_base_class import DataBase


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: FSMContext):

    sql_query = "INSERT INTO users (userid) VALUES (%s) ON CONFLICT DO NOTHING"
    userid = message.from_user.id
    db = DataBase()
    db.insert(sql_query, userid)
    db.close()

    await state.finish()
    await MainState.main_state.set()
    await message.answer('Реакция на команду /start', reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Что делаем?", reply_markup=keyboards['start'])

@dp.callback_query_handler(lambda c: c.data == 'echo', state='*')
async def echo(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Стоп')
    await MainState.echo_state.set()
    await call.answer('Я буду повторять за тобой абсолютно всё!')
    await call.message.answer('Переходим в режим Эхо-бота', reply_markup=keyboard)
    await call.message.answer('Для выхода напиши "Стоп"')

@dp.callback_query_handler(lambda c: c.data == 'parser', state='*')
async def parser(call: types.CallbackQuery):
    await MainState.parser_state.set()
    await call.answer('Попробуем украсть книжку')
    await call.message.answer('Переходим в режим парсера сайта Autor.today', reply_markup=keyboards['parser_auth'])

@dp.callback_query_handler(lambda c: c.data == 'weather', state='*')
async def weather(call: types.CallbackQuery, state: FSMContext):
    sql_query = f"SELECT city FROM users WHERE userid={call.from_user.id}"
    db = DataBase()
    city = db.read_one(sql_query)
    if city[0]:
        sql_query = f"UPDATE users SET city = {city[0]} WHERE userid={call.from_user.id}"
        db.update(sql_query)
        db.close()
        await state.update_data(city=city[0])
        await MainState.weather_state_day.set()
        await call.message.answer('На когда смотрим погоду?', reply_markup=keyboards['weather_day'])
    else:
        await MainState.weather_state.set()
        await call.answer('Погода в выбранном городе')
        await call.message.answer('Введите название города')

@dp.callback_query_handler(lambda c: c.data == 'cheese', state='*')
async def cheese(call: types.CallbackQuery):
    await MainState.cheese_state.set()
    await call.answer('')
    await call.message.answer('Приветствую в сырном отделе!', reply_markup=keyboards['cheese_start'])

@dp.message_handler()
async def error(message: types.Message, state: FSMContext):
    await message.answer('Ты ввёл что-то неправильно. Давай еще раз расскажу,что я могу!',
                         reply_markup=keyboards['start'])
    await MainState.main_state.set()


