import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher


bot = Bot(token=os.environ['TOKEN'])
# Диспетчер для бота
dp = Dispatcher(bot, storage=MemoryStorage())