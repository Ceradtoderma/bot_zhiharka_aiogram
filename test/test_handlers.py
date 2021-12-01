from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from start_handlers import MainState

class TestState(StatesGroup):
    test_state_inline = State()
    test_state_2 = State()

async def save_data(message: types.Message, state: FSMContext):
    data_dict = await state.get_data()
    data_dict['elements'][message.text.split()[0]] = message.text.split()[1]
    await state.update_data(data=data_dict)
    data = await state.get_data()
    for i in data['elements']:
        await message.answer(f'В словаре записано {i}{data["elements"][i]}')

async def answer_inline(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton('Кнопка 1', callback_data='btn1')
    btn_2 = types.InlineKeyboardButton('Кнопка 2', callback_data='btn2')
    keyboard.add(btn_1, btn_2)
    await message.answer('Режим инлайн', reply_markup=keyboard)
    await TestState.test_state_inline.set()


async def inline_test(call: types.CallbackQuery):
    print(call.data)
    if call.data == 'btn1':
        await call.answer('Кнопка 1 нажата!')
        await MainState.main_state.set()
    if call.data == 'btn2':
        await call.answer('Кнопка 2 нажата!')
        await MainState.echo_state.set()
        await call.message.answer('Режим Эхооооооооо')

async def get_state(message: types.Message,state: FSMContext):
    state_now = await state.get_state()
    await message.answer(f'текущее состояние {state_now}')

async def get_data(message: types.Message,state: FSMContext):
    data = await state.get_data()
    await message.answer(f'текущее состояние {data}')



def register_test_handlers(dp: Dispatcher):
    dp.register_message_handler(answer_inline, state=MainState.test_state)
    dp.register_message_handler(get_state, state='*', commands='state')
    dp.register_message_handler(get_data, state='*', commands='data')
    dp.register_callback_query_handler(inline_test, state=TestState.test_state_inline)

