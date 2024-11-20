import asyncio
from json import dumps

import aiohttp
from paho.mqtt.client import Client, CallbackAPIVersion

from shared.config.config import settings
from shared.utils.logger import logger

API = f"http://{settings.API_IP}:{settings.API_PORT}/{settings.API_POSTFIX}"


async def get_all_places() -> list:
    """Получает список мест из API и извлекает их ID."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API}/places") as response:
                if response.status != 200:
                    logger.error(f"Ошибка при получении мест: статус {response.status}")
                    return []

                data = await response.json()

                # Извлекаем список id из ответа
                places = data.get("data", [])
                ids = [place["id"] for place in places if "id" in place]
                return ids
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        return []
    except Exception as e:
        logger.exception(f"Неожиданная ошибка: {e}")
        return []


async def publish_statistic(mqtt_client, place_id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API}/controllers/edge_work_stat/{place_id}') as response:
                if response.status != 200:
                    logger.error(f"Error: Received status {response.status} from API")
                    return

                data = await response.json()

                # Получаем значения с проверкой, если ключи отсутствуют
                meters = data.get('meters', 0.0)
                count = data.get('count', 0)

                # Преобразуем meters к виду с двумя знаками после запятой
                formatted_meters = f"{meters:.2f}"

                topic = f"industrial_statistic_hmi/{place_id}"
                logger.info(f"topic: {topic}")

                message = dumps({'meters': formatted_meters, 'count': count})
                logger.info(f"message: {message}")

                # Публикуем сообщение
                mqtt_client.publish(topic, message)

    except aiohttp.ClientError as e:
        logger.error(f"API request failed: {e}")
    except KeyError as e:
        logger.warning(f"Key missing in response data: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")


async def publish_employees(mqtt_client, place_id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API}/employees/main_on_place/{place_id}') as response:
                if response.status != 200:
                    logger.error(f"Ошибка при получении данных для места {place_id}: статус {response.status}")
                    return

                data = await response.json()
                employee = data.get('data', None)

                topic = f"industrial_hmi/{place_id}"
                logger.info(f"topic: {topic}")

                message = dumps(employee)
                logger.info(f"message: {message}")

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
        tasks = [publish_statistic(client, place) for place in places]
        await asyncio.gather(*tasks)
        await asyncio.sleep(interval)  # Задержка между циклами


async def periodic_employees(client, places, interval=10):
    """Периодически запрашивает и публикует данные сотрудников для заданных мест."""
    while True:
        tasks = [publish_employees(client, place) for place in places]
        await asyncio.gather(*tasks)
        await asyncio.sleep(interval)  # Задержка между циклами


async def main():
    # Получаем список мест
    statistic_places = [25, 29, 30, 32]
    all_places = await get_all_places()

    # Создаем MQTT клиент
    client = Client(client_id=settings.MQTT_CLIENT_ID, callback_api_version=CallbackAPIVersion.VERSION2)
    client.connect(settings.MQTT_HOST, settings.MQTT_PORT)

    try:
        await asyncio.gather(
            periodic_statistic(client, statistic_places),
            periodic_employees(client, all_places)
        )
    finally:
        client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
