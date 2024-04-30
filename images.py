import requests


def get_image(city):
    coords = get_coords(city)
    link = 'http://static-maps.yandex.ru/1.x/'
    search_params = {
        'll': coords,
        'l': 'sat,skl',
        'spn': '0.042069,0.0100552'
    }
    response = requests.get(link, params=search_params)

    # Запишем полученное изображение в файл.

    with open("image.jpg", "wb") as file:
        file.write(response.content)


def get_coords(city):
    params_search = {
        "geocode": city,
        "format": "json",
        "apikey": '40d1649f-0493-4b70-98ba-98533de7710b'
    }
    link = 'http://geocode-maps.yandex.ru/1.x/'
    reponse = requests.get(link, params=params_search)
    data = reponse.json()
    return ','.join(data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split())


def check_get_image(city):
    """
    функция вернет True, если место нашлось. Это сделано, чтобы потом различить,
    отобразить картинку города или картинку того, что город не найден
    """
    try:
        get_image(city)
        return True
    except Exception as e:
        print(e)
        return False
