import requests
from environs import Env
from support_functions import picture_download


NASA_URL_APOD = 'https://api.nasa.gov/planetary/apod'


def get_nasa_download_url(apod_url, api_key, photos_count):
    """
    Получает список URL-адресов фотографий из API NASA.

    Параметры:
        url (str): URL-адрес API NASA для получения фотографий.
        api_key (str): Ключ API NASA для аутентификации запросов.
        photos_count (int): Количество фотографий для получения.

    Возвращает:
        list: Список URL-адресов фотографий.

    Выполняет запрос к API NASA с использованием указанного URL-адреса `url` и параметров запроса, 
    включая ключ API `api_key` и количество фотографий `photos_count`.
    Парсит JSON-ответ и извлекает URL-адреса фотографий, добавляя их в список.
    Возвращает список URL-адресов фотографий.

    Исключения:
        requests.HTTPError: Возникает, если происходит ошибка при выполнении запроса к API NASA.

    Пример использования:
        >>> nasa_url = 'https://api.nasa.gov/planetary/apod'
        >>> api_key = 'YOUR_NASA_API_KEY'
        >>> photos_count = 5
        >>> photos_urls = get_nasa_photos(nasa_url, api_key, photos_count)
    """
    key_count_params = {'api_key': api_key, 'count': photos_count}
    response = requests.get(apod_url, params=key_count_params)
    response.raise_for_status()
    response_elements = response.json()
    urls_list = []
    for element in response_elements:
        url = element['url']
        urls_list.append(url)
    return urls_list


def main():
    env = Env()
    env.read_env()
    nasa_api_key = env.str('NASA_API_KEY')
    picture_download(
        get_nasa_download_url(NASA_URL_APOD, nasa_api_key, 10),
        'pictures', 'nasa_apod'
    )


if __name__ == "__main__":
    main()