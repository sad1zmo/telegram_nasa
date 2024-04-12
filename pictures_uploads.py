import asyncio
import telegram
import os
import random
import time
import argparse
from environs import Env
from pathlib import Path
from telegram import NetworkError



ALL_FILES = []


def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seconds', nargs='?', type=int, default=14400)
    parser.add_argument('-f', '--file', nargs='?', type=str, default='')
 
    return parser


def process_files(directory):
    for current_dir, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(current_dir, file)
            ALL_FILES.append(file_path)
    for subdir in dirs:
            subdir_path = os.path.join(current_dir, subdir)
            process_files(subdir_path)


async def upload_photo_to_telegram(telegram_api_key, time_for_upload, chat_id, file):
     while True:
        process_files(Path('./pictures'))
        random.shuffle(ALL_FILES)
        bot = telegram.Bot(telegram_api_key)
        if file:
            with open(file, 'rb') as file:
                async with bot:
                    await bot.send_document(chat_id=chat_id, document=file)
                    break
        else:
            with open(ALL_FILES[0], 'rb') as document:
                async with bot:
                    await bot.send_document(chat_id=chat_id, document=document)
                    time.sleep(time_for_upload)


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

