import logging
from aiogram import Bot, Dispatcher, executor
from start_handlers import register_handler

from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

TOKEN = os.environ['TOKEN']
print(TOKEN)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot, storage=MemoryStorage())

register_handler(dp)




if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
