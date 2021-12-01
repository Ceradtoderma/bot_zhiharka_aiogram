from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from start_handlers import MainState

async def echo(message: types.Message, state: FSMContext):
    await message.answer(message.text)
    if message.text.lower() == 'стоп':
        await state.finish()
        await message.answer('Эхо-режим выключен')

def register_echo_handlers(dp: Dispatcher):
    dp.register_message_handler(echo, state=MainState.echo_state)