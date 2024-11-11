import asyncio
from json import dumps

import aiohttp
from paho.mqtt.client import Client, CallbackAPIVersion

from shared.config.config import settings

API = f"http://{settings.API_IP}:{settings.API_PORT}/{settings.API_POSTFIX}"


async def statistic(mqtt_client, place_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API}/controllers/edge_work_stat/{place_id}') as response:
            data = await response.json()
            topic = f"industrial_statistic_hmi/{place_id}"
            message = dumps({'meters': round(data['meters'], 2), 'count': data['count']})
            mqtt_client.publish(topic, message)


async def periodic_statistic(client, places, interval=10):
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
