import requests
from pathlib import Path
from urllib.parse import urlparse
import os.path
from environs import Env


NASA_URL_APOD = 'https://api.nasa.gov/planetary/apod'
NASA_EPIC_IMAGES_INFO = 'https://api.nasa.gov/EPIC/api/natural/images'
NASA_EPIC_DOWNLOAD_BASE_URL = 'https://api.nasa.gov/EPIC/archive/natural'
SPACE_X_URL = 'https://api.spacexdata.com/v5/launches'


def picture_download(pictures_urls_list, path, filename):
    """
    Загружает изображения из списка URL-адресов и сохраняет их в указанную директорию.

    Параметры:
        pictures_urls_list (list): Список URL-адресов изображений для загрузки.
        path (str): Путь к директории, в которой будут сохранены изображения.
        filename (str): Имя файла для сохраненных изображений.

    Возвращает:
        None

    Выполняет загрузку изображений из списка URL-адресов `pictures_urls_list`,
    сохраняя каждое изображение в директории `path` с именем файла `filename`
    и добавляя индекс к имени файла для различения изображений.

    Если URL-адрес изображения не содержит расширения файла, он пропускается.

    Исключения:
        requests.HTTPError: Возникает, если происходит ошибка при выполнении запроса к URL-адресу изображения.

    Пример использования:
        >>> pictures_urls = ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']
        >>> picture_download(pictures_urls, 'downloads', 'image')
    """
    Path(path).mkdir(parents=True, exist_ok=True)
    for index, url_picture in enumerate(pictures_urls_list):
        if not get_file_extension(url_picture):
            continue
        response = requests.get(url_picture)
        response.raise_for_status()

        with open(f'{path}/{filename}_{index}.{get_file_extension(url_picture)}', 'wb') as file:
            file.write(response.content)


def get_spacex_photos(url, id):
    """
    Получает оригинальные URL-адреса фотографий SpaceX по идентификатору запуска.

    Параметры:
        url (str): Базовый URL-адрес API SpaceX для получения фотографий.
        id (str): Идентификатор запуска, для которого требуется получить фотографии.

    Возвращает:
        str: Оригинальный URL-адрес фотографий SpaceX для указанного запуска.

    Выполняет запрос к API SpaceX с использованием указанного базового URL-адреса `url` 
    и идентификатора запуска `id`, чтобы получить информацию о фотографиях этого запуска.
    Затем возвращает оригинальный URL-адрес фотографий из JSON-ответа.

    Исключения:
        requests.HTTPError: Возникает, если происходит ошибка при выполнении запроса к API SpaceX.

    Пример использования:
        >>> spacex_url = 'https://api.spacexdata.com/v5/launches'
        >>> launch_id = '5eb87d47ffd86e000604b38a'
        >>> photos_url = get_spacex_photos(spacex_url, launch_id)
    """
    response = requests.get(f'{url}/{id}')
    response.raise_for_status()

    return response.json()['links']['flickr']['original']


# def fetch_spacex_launch(api_url, launch_id):
#     # pictures = get_spacex_photos('https://api.spacexdata.com/v5/launches', '5eb87d47ffd86e000604b38a')
#     pictures = get_spacex_photos(api_url, launch_id)
#     for index, picture in enumerate(pictures):
#         picture_download(picture, 'pictures',
#                          f'space_x_{index}.{get_file_extension(picture)}')


def get_file_extension(url):
    """
    Получает расширение файла из URL-адреса.

    Параметры:
        url (str): URL-адрес файла.

    Возвращает:
        str: Расширение файла без точки.

    Выполняет разбор URL-адреса с использованием модуля `urlparse` для получения пути к файлу.
    Затем извлекает имя файла и его расширение с помощью функции `os.path.splitext`.
    Возвращает расширение файла без точки.

    Пример использования:
        >>> url = 'https://example.com/image.jpg'
        >>> extension = get_file_extension(url)
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    (file_path, file) = os.path.split(path)
    (file_name, extension) = os.path.splitext(file)
    return extension[1:]


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


def get_nasa_epic_download_url(base_url, info_url, api_key, extention):
    """
    Получает список URL-адресов для скачивания изображений из API NASA EPIC.

    Параметры:
        base_url (str): Базовый URL-адрес для скачивания изображений.
        info_url (str): URL-адрес API для получения информации о изображениях.
        api_key (str): Ключ API NASA EPIC для аутентификации запросов.
        extension (str): Расширение файлов изображений.

    Возвращает:
        list: Список URL-адресов для скачивания изображений.

    Выполняет запрос к API NASA EPIC с использованием указанного URL-адреса `info_url` 
    и ключа API `api_key`, чтобы получить информацию о изображениях.
    Для каждого изображения создает URL-адрес скачивания, включая дату, расширение и имя файла,
    а также добавляя параметр `api_key` для аутентификации запроса.
    Возвращает список URL-адресов для скачивания изображений.

    Исключения:
        requests.HTTPError: Возникает, если происходит ошибка при выполнении запроса к API NASA EPIC.

    Пример использования:
        >>> base_url = 'https://epic.gsfc.nasa.gov/archive/natural'
        >>> info_url = 'https://epic.gsfc.nasa.gov/api/natural'
        >>> api_key = 'YOUR_NASA_EPIC_API_KEY'
        >>> extension = 'jpg'
        >>> urls = get_nasa_epic_download_url(base_url, info_url, api_key, extension)
    """
    payload = {'api_key': api_key}
    response = requests.get(info_url, params=payload)
    response.raise_for_status()
    pictures_info_list = response.json()
    urls_list = []
    for index, picture_info in enumerate(pictures_info_list):
        image_name = picture_info['image']
        (date, time) = picture_info['date'].split(' ')
        date = date.replace('-', '/')

        link = f'{base_url}/{date}/{extention}/{image_name}.{extention}?api_key={api_key}'
        urls_list.append(link)
    return urls_list


def main():
    env = Env()
    env.read_env()
    nasa_api_key = env.str('NASA_API_KEY')
    space_x_launch_id = env.str('SPACE_X_LAUNCH_ID')
    picture_download(
        get_spacex_photos(SPACE_X_URL, space_x_launch_id),
        'pictures', 'space-x'
    )
    picture_download(
        get_nasa_epic_download_url(
            NASA_EPIC_DOWNLOAD_BASE_URL,
            NASA_EPIC_IMAGES_INFO,
            nasa_api_key, 'png'),
        'pictures', 'nasa_epic'
    )
    picture_download(
        get_nasa_download_url(NASA_URL_APOD, nasa_api_key, 10),
        'pictures', 'nasa_apod'
    )


if __name__ == "__main__":
    main()
