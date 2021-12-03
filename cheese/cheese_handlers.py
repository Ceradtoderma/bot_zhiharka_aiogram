from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from cheese.data_base_class import DataBase
from start_handlers import MainState

from keyboards import keyboards
import threading


class CheeseState(StatesGroup):
    main_state = State()


class AddCheese(StatesGroup):
    add_name = State()
    add_price = State()
    add_description = State()
    add_img = State()
    insert = State()



async def main_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'all_cheese':
        await call.message.answer('Посмотрим все сыры, которые у нас есть!')
        db = DataBase()
        res = db.read_all()
        print(res)
        db.close()
        await call.message.answer(res)
        await call.answer()
    if call.data == 'add_cheese':
        await call.message.answer('Давайте добавим новый сыр')
        await call.message.answer('Название?')
        await AddCheese.add_name.set()


async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Цена?')
    await AddCheese.next()

async def add_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        price = int(message.text)
        await state.update_data(price=price)
        await message.answer('Расскажи что-нибудь о нем')
        await AddCheese.next()
    else:
        await message.answer('Цена может быть только числом')

async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Картинка?')
    await AddCheese.next()


async def add_img(message: types.Message, state: FSMContext):
    await state.update_data(img=message.text)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Добавить в базу данных', callback_data='add'))
    await message.answer('Все данные получены', reply_markup=keyboard)
    # data = await state.get_data()
    # print(data)
    await AddCheese.next()

async def insert(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Мы попали в инсерт')
    data = await state.get_data()
    args = (data['name'], data['price'], data['description'], data['img'])
    db = DataBase(*args)
    db.insert()
    if db.err:
        await call.message.answer(db.err)
    else:
        await call.message.answer('Данные добавлены', reply_markup=keyboards['cheese_start'])
    db.close()
    await MainState.cheese_state.set()


def register_cheese_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(main_handler, state=MainState.cheese_state)
    dp.register_message_handler(add_name, state=AddCheese.add_name)
    dp.register_message_handler(add_price, state=AddCheese.add_price)
    dp.register_message_handler(add_description, state=AddCheese.add_description)
    dp.register_message_handler(add_img, state=AddCheese.add_img)
    dp.register_callback_query_handler(insert, state=AddCheese.insert)