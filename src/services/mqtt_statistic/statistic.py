import asyncio
from json import dumps

import aiohttp
from src.config import settings
from gmqtt import Client as MQTTClient

API = "http://192.168.21.1:8000/api"
MQTT = {"host": "192.168.20.240", "port": 1883, "username": "", "password": ""}


async def get_edge_work_stat(session, place_id: int) -> dict:
    async with session.get(f'{API}/controllers/edge_work_stat/{place_id}') as response:
        data = await response.json()
        return {"data": data['count'], "meters": data['meters']}


async def publish_work_stat(client, session, place_id):
    topic = f"industrial_hmi_stat/{place_id}"
    work_stat = await get_edge_work_stat(session, place_id)
    message = dumps(work_stat)
    client.publish(topic, message)


async def main():
    places = [25, 29, 30, 32]

    async with aiohttp.ClientSession() as session:
        client = MQTTClient("client_hmi_stat")
        await client.connect(settings.MQTT_HOST, port=settings.MQTT_PORT)

        publish_tasks = [publish_work_stat(client, session, place) for place in places]
        await asyncio.gather(*publish_tasks)

        await client.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()


    async def periodic_main():
        while True:
            await main()
            await asyncio.sleep(1)  # Interval in seconds


    loop.run_until_complete(periodic_main())
