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
            message = dumps({'meters': data['meters'], 'count': data['count']})
            mqtt_client.publish(topic, message)


async def main():
    places = [25, 29, 30, 32]
    client = Client(client_id=settings.MQTT_CLIENT_ID, callback_api_version=CallbackAPIVersion.VERSION2)
    client.connect(settings.MQTT_HOST, settings.MQTT_PORT)

    tasks = []
    for place in places:
        tasks.append(statistic(client, place))
        await asyncio.sleep(5)  # Ограничение на 5 секунд между запросами для каждого place

    await asyncio.gather(*tasks)
    client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
