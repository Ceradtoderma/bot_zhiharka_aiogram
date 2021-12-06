from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from cheese.data_base_class import DataBase
from start_handlers import MainState
from cheese.func import upload_photo
from keyboards import keyboards
from bot import bot, dp


class CheeseState(StatesGroup):
    main_state = State()
    choise = State()


class AddCheese(StatesGroup):
    add_name = State()
    add_price = State()
    add_description = State()
    add_img = State()
    insert = State()

@dp.callback_query_handler(state=MainState.cheese_state)
async def main_handler(call: types.CallbackQuery):
    if call.data == 'all_cheese':
        await call.message.answer('Посмотрим все сыры, которые у нас есть!')
        db = DataBase()
        res = db.read_all()
        db.close()
        keyboard = types.InlineKeyboardMarkup()
        for i in res:
            keyboard.add(types.InlineKeyboardButton(text=i[1], callback_data=i[0]))

        await call.message.answer('Выбирай!', reply_markup=keyboard)
        await CheeseState.choise.set()
        await call.answer()
    if call.data == 'add_cheese':
        await call.message.answer('Давайте добавим новый сыр')
        await call.message.answer('Название?')
        await AddCheese.add_name.set()


@dp.callback_query_handler(state=CheeseState.choise)
async def choise(call: types.CallbackQuery):
    db = DataBase(call.data)
    res = db.read_id()
    await call.message.answer(res[1])
    await call.message.answer(f'Цена: {res[2]}')
    await call.message.answer(res[4])
    await call.message.answer(res[3])

@dp.message_handler(state=AddCheese.add_name)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Цена?')
    await AddCheese.next()

@dp.message_handler(state=AddCheese.add_price)
async def add_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        price = int(message.text)
        await state.update_data(price=price)
        await message.answer('Расскажи что-нибудь о нем')
        await AddCheese.next()
    else:
        await message.answer('Цена может быть только числом')

@dp.message_handler(state=AddCheese.add_description)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Картинка?')
    await AddCheese.next()

@dp.message_handler(state=AddCheese.add_img)
async def add_img(message: types.Message, state: FSMContext):
    await state.update_data(url_img=message.text)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Добавить в базу данных', callback_data='add'))
    await message.answer('Все данные получены', reply_markup=keyboard)
    await AddCheese.next()

@dp.callback_query_handler(state=AddCheese.insert)
async def insert(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    img = upload_photo(data['url_img'], data['name'])
    args = (data['name'], data['price'], data['description'], img)
    db = DataBase(*args)
    db.insert()
    if db.err:
        await call.message.answer(db.err)
    else:
        await call.message.answer('Данные добавлены', reply_markup=keyboards['cheese_start'])
    db.close()
    await call.answer('Данные добавлены')
    await MainState.cheese_state.set()


