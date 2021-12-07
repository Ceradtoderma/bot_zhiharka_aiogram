import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup


class MainState(StatesGroup):
    main_state = State()
    parser_state = State()
    echo_state = State()
    test_state = State()
    weather_state = State()
    cheese_state = State()


bot = Bot(token=os.environ['TOKEN'])
# Диспетчер для бота
dp = Dispatcher(bot, storage=MemoryStorage())