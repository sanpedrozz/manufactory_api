from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Place, AlarmMessages, AlarmHistory
from src.alarm_service.schemas import Alarm
from src.telegram_bot.services import send_message


async def alarm_message(db: AsyncSession, alarm: Alarm, dt):
    # Сборка данных для сообщения
    place = await Place.get_place_by_id(db, alarm.place_id)
    alarm_data = await AlarmMessages.get_alarm_by_id(db, alarm.alarm)

    # Сборка сообщения
    message = (f'Место аварии: {place.name}\n'
               f'Точное время: {dt}\n'
               f'Авария: {alarm_data.message}\n'
               f'Комментарий: {alarm.comment if alarm.comment else "Отсутствует"}\n'
               f'{alarm_data.tag}')

    await send_message(message, place.message_thread_id)


async def add_alarm_history(db: AsyncSession, alarm: Alarm, dt):
    new_alarm_history = AlarmHistory(
        place_id=alarm.place_id,
        alarm_id=alarm.alarm,
        comments=alarm.comment if alarm.comment else "",
        dt_created=dt
    )
    await new_alarm_history.add(db)
    return new_alarm_history
