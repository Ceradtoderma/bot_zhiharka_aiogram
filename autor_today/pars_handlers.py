from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from autor_today.parser import ParsAT
from start_handlers import MainState
from keyboards import keyboards
import threading



class Parser_State(StatesGroup):
    login_state = State()
    password_state = State()
    ready_state = State()
    to_go = State()


async def auth(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'login':
        await call.message.answer('Введите логин')
        await Parser_State.login_state.set()
    else:
        await state.update_data(login='0')
        await Parser_State.ready_state.set()
        await call.message.answer('Введите ссылку')


async def get_login(message: types.Message, state: FSMContext):
    if '@' in message.text:
        await state.update_data(login=message.text.lower())
        await message.answer('Введите пароль')
        await Parser_State.next()
    else:
        await message.answer('Введите корректный логин')

async def get_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer('Введите ссылку')
    await Parser_State.next()

async def get_ready(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text.lower())
    user_data = await state.get_data()
    await Parser_State.to_go.set()
    if user_data['login'] == '0':
        await message.answer(f'Пытаемся спарсить без входа на сайт ссылка на книгу {user_data["url"]}',
                             reply_markup=keyboards['parser_start'])
    else:
        await message.answer(f'Итак данные: логин: {user_data["login"]}, пароль: {user_data["password"]}, '
                             f'ссылка на книгу: {user_data["url"]}')
        await message.answer('Начать парсинг?', reply_markup=keyboards['parser_start'])

async def to_go(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    cur_page = ''
    try:
        if user_data['login'] == '0':
            par = ParsAT(user_data['url'])
            threading.Thread(target=par.get_text).start()
        else:
            par = ParsAT(user_data['url'], user_data['login'], user_data['password'])
            threading.Thread(target=par.login).start()

        while par.pars:
            if cur_page == par.cur_chapter:
                continue
            else:
                cur_page = par.cur_chapter
                await call.message.answer(str(cur_page))
        if par.state != 'ok':
            await call.message.answer('Ошибка! текст ошибки: ')
            if par.error == 'Неверный логин или пароль.':
                await Parser_State.login_state.set()
                await call.message.answer(f'"{par.error}"')
                await call.message.answer('Введите логин')
            else:
                await call.message.answer(f'"{par.error}"')
                await Parser_State.ready_state.set()
                if user_data.get('password', "0") == '0':
                    await call.message.answer('Попробуйте ввести ссылку еще раз', reply_markup=keyboards['parser_login'])
                else:
                    await call.message.answer('Попробуйте ввести ссылку еще раз')

        else:
            await call.message.answer('Парсинг завершен')

            try:
                await call.message.reply_document(open(par.name + '.txt', 'rb'))
            except:
                await call.message.answer('Парсинг не удался')

            await Parser_State.ready_state.set()
            await call.message.answer('Спарсим еще что-нибудь? Введите ссылку')

    except:
        await call.message.answer('Ошибка сервера')
    finally:
        await call.answer('')



async def error(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('login', '1') == '1':
        await message.answer('Нужно выбрать будем логиниться или нет')
    else:
        await message.answer('Нужно Начать парсинг')


def register_pars_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(auth, state=[MainState.parser_state, Parser_State.ready_state])
    dp.register_message_handler(get_login, state=Parser_State.login_state)
    dp.register_message_handler(get_password, state=Parser_State.password_state)
    dp.register_message_handler(get_ready, state=Parser_State.ready_state)
    dp.register_callback_query_handler(to_go, state=Parser_State.to_go)

    dp.register_message_handler(error, state=[MainState.parser_state, Parser_State.to_go])
