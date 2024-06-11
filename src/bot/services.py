# src/bot/services.py

from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from typing import List

from src.config import settings

bot = Bot(token=settings.BOT_TOKEN)


async def send_video(paths: List[str], message: str):
    try:
        media_group = MediaGroupBuilder(caption=message)

        for path in paths:
            video = FSInputFile(path)
            media_group.add(type="video", media=video)

        await bot.send_media_group(chat_id=settings.CHAT_ID, media=media_group.build())
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
