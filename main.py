import logging
from aiogram import Bot, Dispatcher, executor
import start_handlers
import autor_today.pars_handlers
import cheese.cheese_handlers
import weather.weather_handlers
import echo.echo_handlers
from bot import bot, dp


logging.basicConfig(level=logging.INFO)





if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
