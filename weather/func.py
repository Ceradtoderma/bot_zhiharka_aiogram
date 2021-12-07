import requests

weather_api = 'https://api.openweathermap.org/data/2.5/onecall'
api_weather_key = 'fc3837d82e69a8bea3f8c2a0f1e68643'
weather_coord = 'http://api.openweathermap.org/data/2.5/weather'


def find_city(name):
    param = {
        'q': name,
        'appid': api_weather_key
    }

    response = requests.get(weather_coord, params=param).json()
    lon, lat = response['coord']['lon'], response['coord']['lat']
    return lon, lat


def get_data_old(lon, lat, day):

    weather_data = {}
    param = {
        'appid': api_weather_key,
        'exclude': 'current, hourly',
        'lang': 'ru',
        'lat': lat,
        'lon': lon,
        'units': 'metric'
    }
    response = requests.get(weather_api, params=param).json()

    weather_data['temp_morn'] = response['daily'][day]['temp']['morn']
    weather_data['temp_day'] = response['daily'][day]['temp']['day']
    weather_data['temp_eve'] = response['daily'][day]['temp']['eve']
    weather_data['temp_night'] = response['daily'][day]['temp']['night']
    weather_data['feels_like_morn'] = response['daily'][day]['feels_like']['morn']
    weather_data['feels_like_day'] = response['daily'][day]['feels_like']['day']
    weather_data['feels_like_eve'] = response['daily'][day]['feels_like']['eve']
    weather_data['feels_like_night'] = response['daily'][day]['feels_like']['night']
    weather_data['clouds'] = response['daily'][day]['clouds']
    weather_data['description'] = response['daily'][day]['weather'][0]['description']

    return weather_data

def get_data(lon, lat, day):
    weather_data = {}
    param = {
        'appid': api_weather_key,
        'exclude': 'current, hourly',
        'lang': 'ru',
        'lat': lat,
        'lon': lon,
        'units': 'metric'
    }
    response = requests.get(weather_api, params=param).json()['daily'][day]

    weather_data['temp_morn'] = int(response['temp']['morn'])
    weather_data['temp_day'] = int(response['temp']['day'])
    weather_data['temp_eve'] = int(response['temp']['eve'])
    weather_data['temp_night'] = int(response['temp']['night'])
    weather_data['feels_like_morn'] = int(response['feels_like']['morn'])
    weather_data['feels_like_day'] = int(response['feels_like']['day'])
    weather_data['feels_like_eve'] = int(response['feels_like']['eve'])
    weather_data['feels_like_night'] = int(response['feels_like']['night'])
    weather_data['clouds'] = response['clouds']
    weather_data['description'] = response['weather'][0]['description']
    weather_data['url_ico'] = f"http://openweathermap.org/img/wn/{response['weather'][0]['icon']}@4x.png"

    return weather_data


if __name__ == '__main__':
    lon, lat = find_city('Ростов-на-Дону')
    print(get_data(lon, lat, 0))
