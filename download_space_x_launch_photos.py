import requests
import argparse
from support_functions import picture_download
from pathlib import Path


SPACE_X_URL = 'https://api.spacexdata.com/v5/launches'
SPACE_X_LAUNCH_ID = '5eb87d47ffd86e000604b38a'


def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-i', '--id', nargs='?', default=SPACE_X_LAUNCH_ID)
    parser.add_argument ('-f', '--download_path', nargs='?', default='pictures')
 
    return parser


def get_spacex_photo_urls(url, launch_id):
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
    response = requests.get(f'{url}/{launch_id}')
    response.raise_for_status()

    return response.json()['links']['flickr']['original']


def main():
    args = create_parser().parse_args()
    space_x_launch_id = args.id
    download_path = args.download_path
    Path(download_path).mkdir(parents=True, exist_ok=True)
    picture_download(
        get_spacex_photo_urls(SPACE_X_URL, space_x_launch_id),
        download_path, 'space-x'
    )


if __name__ == "__main__":
    main()