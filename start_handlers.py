from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import keyboards
from states import MainState


from autor_today.pars_handlers import register_pars_handlers
from echo.echo_handlers import register_echo_handlers
from weather.weather_handlers import register_weather_handlers
from cheese.cheese_handlers import register_cheese_handlers




async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await MainState.main_state.set()
    await message.answer('Реакция на команду /start')
    await message.answer("Что делаем?", reply_markup=keyboards['start'])



async def inline_answer(call: types.CallbackQuery):
    if call.data == 'echo':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Стоп')
        await MainState.echo_state.set()
        await call.answer('Я буду повторять за тобой абсолютно всё!')
        await call.message.answer('Переходим в режим Эхо-бота', reply_markup=keyboard)
        await call.message.answer('Для выхода напиши "Стоп"')

    if call.data == 'parser':
        await MainState.parser_state.set()
        await call.answer('Попробуем украсть книжку')
        await call.message.answer('Переходим в режим парсера сайта Autor.today', reply_markup=keyboards['parser_auth'])

    if call.data == 'weather':
        await MainState.weather_state.set()
        await call.answer('Погода в выбранном городе')
        await call.message.answer('Введите название города')

    if call.data == 'cheese':
        await MainState.cheese_state.set()
        await call.answer('')
        await call.message.answer('Приветствую в сырном отделе!', reply_markup=keyboards['cheese_start'])



async def error(message: types.Message, state: FSMContext):
    await message.answer('Ты ввёл что-то неправильно. Давай еще раз расскажу,что я могу!',
                         reply_markup=keyboards['start'])
    await MainState.main_state.set()


def register_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_callback_query_handler(inline_answer, state=MainState.main_state)
    register_weather_handlers(dp)
    register_echo_handlers(dp)
    register_pars_handlers(dp)
    register_cheese_handlers(dp)

    dp.register_message_handler(error, state='*')