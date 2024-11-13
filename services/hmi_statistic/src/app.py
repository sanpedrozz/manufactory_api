import asyncio
from json import dumps

import aiohttp
from paho.mqtt.client import Client, CallbackAPIVersion

from shared.config.config import settings
from shared.utils.logger import logger

API = f"http://{settings.API_IP}:{settings.API_PORT}/{settings.API_POSTFIX}"


async def statistic(mqtt_client, place_id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API}/controllers/edge_work_stat/{place_id}') as response:
                if response.status != 200:
                    logger.error(f"Error: Received status {response.status} from API")
                    return
                else:
                    logger.info(f"response")

                data = await response.json()

                # Получаем значения с проверкой, если ключи отсутствуют
                meters = data.get('meters', 0.0)
                count = data.get('count', 0)

                # Преобразуем meters к виду с двумя знаками после запятой
                formatted_meters = f"{meters:.2f}"

                topic = f"industrial_statistic_hmi/{place_id}"
                message = dumps({'meters': formatted_meters, 'count': count})

                # Публикуем сообщение
                mqtt_client.publish(topic, message)

    except aiohttp.ClientError as e:
        logger.error(f"API request failed: {e}")
    except KeyError as e:
        logger.warning(f"Key missing in response data: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")


async def periodic_statistic(client, places, interval=5):
    """Периодически выполняет сбор статистики для заданных мест."""
    while True:
        tasks = [statistic(client, place) for place in places]
        await asyncio.gather(*tasks)
        await asyncio.sleep(interval)  # Задержка между циклами


async def main():
    # await asyncio.sleep(10)
    places = [25, 29, 30, 32]
    client = Client(client_id=settings.MQTT_CLIENT_ID, callback_api_version=CallbackAPIVersion.VERSION2)
    client.connect(settings.MQTT_HOST, settings.MQTT_PORT)

    try:
        await periodic_statistic(client, places)
    finally:
        client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
