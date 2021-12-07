from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from cheese.data_base_class import DataBase
from start_handlers import MainState
from cheese.func import upload_photo
from keyboards import keyboards
from bot import dp
import aiogram.utils.markdown as fmt


class CheeseState(StatesGroup):
    choise = State()
    one_cheese = State()
    edit = State()


class AddCheese(StatesGroup):
    add_name = State()
    add_price = State()
    add_description = State()
    add_img = State()
    insert = State()


# Работают всегда
@dp.callback_query_handler(lambda c: c.data == 'all_cheese', state='*')
async def all_cheese(call: types.CallbackQuery):
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


@dp.callback_query_handler(lambda c: c.data == 'add_cheese', state='*')
async def add_cheese(call: types.CallbackQuery):
    await call.message.answer('Давайте добавим новый сыр')
    await call.message.answer('Название?')
    await AddCheese.add_name.set()
    await call.answer()


@dp.callback_query_handler(lambda c: c.data == 'one_cheese', state='*')
async def one_cheese(call: types.CallbackQuery):
    await call.message.answer('Напишите название')
    await CheeseState.one_cheese.set()
    await call.answer()


@dp.callback_query_handler(lambda c: c.data == 'del', state='*')
async def delete(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db = DataBase()
    db.delete(data['id'])
    db.close()
    await call.message.answer('Удалено', reply_markup=keyboards['cheese_start'])


@dp.callback_query_handler(lambda c: c.data == 'edit', state='*')
async def edit(call: types.CallbackQuery, state: FSMContext):
    await CheeseState.edit.set()
    await call.message.answer('Что редактируем?', reply_markup=keyboards['cheese_edit'])
    await call.message.answer('Изменено', reply_markup=keyboards['cheese_start'])


# состояние поиска по имени one_cheese

@dp.message_handler(state=CheeseState.one_cheese)
async def one_cheese(message: types.Message, state: FSMContext):
    db = DataBase()
    res = db.read_name(message.text)
    if len(res) == 1:
        one_cheese = db.read_id(res[0][0])
        await state.update_data(id=res[0][0])
        await MainState.cheese_state.set()
        await message.answer(f'{fmt.hide_link(one_cheese[4])}{one_cheese[1]}\nЦена: {one_cheese[2]}',
                             parse_mode=types.ParseMode.HTML)
        await message.answer(one_cheese[3], reply_markup=keyboards['cheese_del'])

    elif len(res) > 1:
        print('Много сыров!')
        keyboard = types.InlineKeyboardMarkup()
        for i in res:
            keyboard.add(types.InlineKeyboardButton(text=i[1], callback_data=i[0]))
        await CheeseState.choise.set()
        await message.answer('Выбирай!', reply_markup=keyboard)

    else:
        await message.answer('Нет совпадений')
    db.close()


# Состояние выбора из вариантов
@dp.callback_query_handler(state=CheeseState.choise)
async def choise(call: types.CallbackQuery, state: FSMContext):
    db = DataBase()
    res = db.read_id(call.data)
    await state.update_data(id=call.data)
    await MainState.cheese_state.set()
    await call.message.answer(f'{fmt.hide_link(res[4])}{res[1]}\nЦена: {res[2]}', parse_mode=types.ParseMode.HTML)
    await call.message.answer(res[3], reply_markup=keyboards['cheese_del'])


# Добавление нового сыра шаг за шагом
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
    try:
        img = upload_photo(data['url_img'], data['name'])
    except:
        img = data['url_img']
    args = (data['name'], data['price'], data['description'], img)
    db = DataBase()
    db.insert(*args)
    if db.err:
        await call.message.answer(db.err)
    else:
        await call.message.answer('Данные добавлены', reply_markup=keyboards['cheese_start'])
    db.close()
    await call.answer('Данные добавлены')
    await MainState.cheese_state.set()


# Реакция на фото
@dp.message_handler(content_types=["photo"], state=AddCheese.add_img)
async def download_photo(message: types.Message, state: FSMContext):
    url = await message.photo[-1].get_url()
    await state.update_data(url_img=url)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Добавить в базу данных', callback_data='add'))
    await message.answer('Все данные получены', reply_markup=keyboard)
    await AddCheese.next()
