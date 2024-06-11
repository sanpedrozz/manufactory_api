from aiogram import Bot
from aiogram.types import FSInputFile

from src.config import settings

bot = Bot(token=settings.BOT_TOKEN)


async def send_video(path_file: str, message: str):
    try:
        video = FSInputFile(path_file)
        await bot.send_video(chat_id=settings.CHAT_ID, video=video, caption=message)
    except Exception as e:
        error_message = f"{message}\n\nВидео отправить не получилось: {e}"
        await bot.send_message(chat_id=settings.CHAT_ID, text=error_message)
    finally:
        await bot.session.close()


async def send_message(message: str):
    try:
        await bot.send_message(chat_id=settings.CHAT_ID, text=message)
    except Exception as e:
        error_message = f"Сообщение отправить не получилось: {e}"
        await bot.send_message(chat_id=settings.CHAT_ID, text=error_message)
    finally:
        await bot.session.close()
