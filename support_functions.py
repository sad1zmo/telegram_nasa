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