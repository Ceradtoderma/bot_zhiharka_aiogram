from aiogram.dispatcher.filters.state import State, StatesGroup


class MainState(StatesGroup):
    main_state = State()
    parser_state = State()
    echo_state = State()
    test_state = State()
    weather_state = State()
    cheese_state = State()