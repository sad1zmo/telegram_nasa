import requests
from pathlib import Path
from urllib.parse import urlparse
import os.path


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


def download_pictures(picture_urls, path, filename, api_key='q='):
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
    payload = {'api_key': api_key}
    for index, picture_url in enumerate(picture_urls):
        if not get_file_extension(picture_url):
            continue
        response = requests.get(picture_url, params=payload)
        response.raise_for_status()

        file_path = Path(path, f"{filename}_{index}.{get_file_extension(
            picture_url)}")
        with open(file_path, 'wb') as file:
            file.write(response.content)
