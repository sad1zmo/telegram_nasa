import requests
from environs import Env
from support_functions import picture_download


NASA_EPIC_IMAGES_INFO = 'https://api.nasa.gov/EPIC/api/natural/images'
NASA_EPIC_DOWNLOAD_BASE_URL = 'https://api.nasa.gov/EPIC/archive/natural'


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
    for picture_info in pictures_info_list:
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
    
    picture_download(
        get_nasa_epic_download_url(
            NASA_EPIC_DOWNLOAD_BASE_URL,
            NASA_EPIC_IMAGES_INFO,
            nasa_api_key, 'png'),
        'pictures', 'nasa_epic'
    )


if __name__ == "__main__":
    main()
