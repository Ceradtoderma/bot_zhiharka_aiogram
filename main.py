import logging
from aiogram import Bot, Dispatcher, executor
from start_handlers import register_handler
from bot import bot, dp

logging.basicConfig(level=logging.INFO)


register_handler(dp)




if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
