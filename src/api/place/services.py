from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Place


async def get_all_places(db: AsyncSession):
    """
    Получить список всех устройств (Place)
    """
    return await Place.get_all(db)


# async def add_(db: AsyncSession, alarm: Alarm, dt):
#     new_alarm_history = AlarmHistory(
#         place_id=alarm.place_id,
#         alarm_id=alarm.alarm,
#         comments=alarm.comment if alarm.comment else "",
#         dt_created=dt
#     )
#     await new_alarm_history.add(db)

