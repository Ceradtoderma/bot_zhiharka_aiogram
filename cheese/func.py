import requests
import transliterate

def upload_photo(url_photo, name):
    URL = 'https://api.imgbb.com/1/upload'
    API_KEY = '725eaaa1b4ead13d43c756a1c2c5f566'
    param = {'key': API_KEY}
    data = {'image': url_photo,
            'name': transliterate.translit(name, language_code='ru', reversed=True)}
    res = requests.post(URL, params=param, data=data)
    return res.json()['data']['image']['url']
