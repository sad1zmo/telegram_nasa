import requests
from environs import Env
from support_functions import picture_download
from datetime import datetime
from pathlib import Path
import argparse


NASA_EPIC_IMAGES_INFO = 'https://api.nasa.gov/EPIC/api/natural/images'
NASA_EPIC_DOWNLOAD_BASE_URL = 'https://api.nasa.gov/EPIC/archive/natural'


def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-f', '--download_path', nargs='?', default='pictures')
 
    return parser


def get_nasa_epic_download_urls(base_url, info_url, api_key, extention):
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
    epic_download_url_list = []
    for picture_info in pictures_info_list:
        image_name = picture_info['image']
        (date, time) = picture_info['date'].split(' ')
        datetime_from_string = datetime.strptime(date, "%Y-%m-%d")
        date = datetime_from_string.strftime("%Y/%m/%d")
        link = f'{base_url}/{date}/{extention}/{image_name}.{extention}'
        epic_download_url_list.append(link)
    return epic_download_url_list


def main():
    env = Env()
    env.read_env()
    nasa_api_key = env.str('NASA_API_KEY')
    args = create_parser().parse_args()
    download_path = args.download_path
    Path(download_path).mkdir(parents=True, exist_ok=True)
    
    picture_download(
        get_nasa_epic_download_urls(
            NASA_EPIC_DOWNLOAD_BASE_URL,
            NASA_EPIC_IMAGES_INFO,
            nasa_api_key, 'png'),
        download_path, 'nasa_epic', nasa_api_key
    )


if __name__ == "__main__":
    main()
