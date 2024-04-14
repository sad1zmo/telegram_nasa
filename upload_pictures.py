import asyncio
import telegram
import os
import random
import time
import argparse
from environs import Env
from pathlib import Path
from telegram.error import NetworkError



ALL_FILES = []


def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seconds', nargs='?', type=int, default=14400)
    parser.add_argument('-f', '--file', nargs='?', type=str, default='')
 
    return parser


def collect_process_files(directory):
    for file_path in Path(directory).rglob('*'):
        if file_path.is_file():
            ALL_FILES.append(file_path)


async def send_document(bot, chat_id, file_path, time_for_upload=None):
    async with bot:
        with open(file_path, 'rb') as file:
            await bot.send_document(chat_id=chat_id, document=file)
    if time_for_upload:
        time.sleep(time_for_upload)


async def upload_photo_to_telegram(telegram_api_key, time_for_upload, chat_id, file):
     while True:
        collect_process_files(Path('./pictures'))
        random.shuffle(ALL_FILES)
        bot = telegram.Bot(telegram_api_key)
        if file:
            await send_document(bot, chat_id, file)
        else:
            await send_document(bot, chat_id, ALL_FILES[0], time_for_upload)


async def main():
    env = Env()
    env.read_env()
    telegram_api_key = env.str('TELEGRAM_API_KEY')
    chat_id = env.str('TELEGRAM_CHAT_ID')
    args = create_parser().parse_args()
    time_for_upload = args.seconds
    file_for_upload = args.file
    try:
        await upload_photo_to_telegram(telegram_api_key, time_for_upload, chat_id, file_for_upload)
    except NetworkError:
        print("Проблемы с сетью. Повторная попытка через 60 секунд")
        time.sleep(60)

        
if __name__ == "__main__":
    asyncio.run(main())

