from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.db.models import Place, AlarmMessages
from src.alarm_service.schemas import Alarm
from src.telegram_bot.services import send_message


async def alarm_message(alarm: Alarm, db: AsyncSession):
    current_time = datetime.now()

    # Сборка данных для сообщения
    place = await Place.get_place_by_id(db, alarm.place_id)
    alarm_data = await AlarmMessages.get_alarm_by_id(db, alarm.alarm)

    # Сборка сообщения
    message = (f'Место аварии: {place.name}\n'
               f'Точное время: {current_time}\n'
               f'Авария: {alarm_data.message}\n'
               f'Комментарий: {alarm.comment if alarm.comment else "Отсутствует"}\n'
               f'{alarm_data.tag}')

    await send_message(message, place.message_thread_id)
