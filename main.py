import asyncio
import telegram


async def main():
    bot = telegram.Bot('6862815577:AAEyGruttYZBghOS_gHyNKIZkbGLlO2icv8')
    async with bot:
        updates = (await bot.send_message(chat_id='@picha_nasa', text="I'm sorry Dave I'm afraid I can't do that."))
        print(updates)



if __name__ == "__main__":
    asyncio.run(main())

