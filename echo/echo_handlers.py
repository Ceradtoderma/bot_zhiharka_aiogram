from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import keyboards
from start_handlers import MainState
from bot import dp


@dp.message_handler(state=MainState.echo_state)
async def echo(message: types.Message, state: FSMContext):
    await message.answer(message.text)
    if message.text.lower() == 'стоп':
        await state.finish()
        await message.answer('Эхо-режим выключен', reply_markup=keyboards['start'])
