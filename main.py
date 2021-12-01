import logging
from aiogram import Bot, Dispatcher, executor
from start_handlers import register_handler

from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(token="1147643880:AAFi5gJPjpNsOmz240w95RtxC9LCKfPAJ4M")
# Диспетчер для бота
dp = Dispatcher(bot, storage=MemoryStorage())

register_handler(dp)




if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
