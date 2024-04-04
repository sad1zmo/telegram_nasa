import asyncio
import telegram
import os
import random
import time
import argparse
from environs import Env


ALL_FILES = []


def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--secconds', nargs='?', type=int, default=14400)
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


async def upload_photo_to_telegram(telegram_api_key, time_for_upload, file):
     while True:
        process_files('./pictures')
        random.shuffle(ALL_FILES)
        bot = telegram.Bot(telegram_api_key)
        if file:
            async with bot:
                await bot.send_document(chat_id='@picha_nasa', document=open(file, 'rb'))
                break
        else:
            async with bot:
                await bot.send_document(chat_id='@picha_nasa', document=open(ALL_FILES[0], 'rb'))
                time.sleep(time_for_upload)


async def main():
    env = Env()
    env.read_env()
    telegram_api_key = env.str('TELEGRAM_API_KEY')
    args = create_parser().parse_args()
    time_for_upload = args.secconds
    file_for_upload = args.file
    await upload_photo_to_telegram(telegram_api_key, time_for_upload, file_for_upload)

if __name__ == "__main__":
    asyncio.run(main())

