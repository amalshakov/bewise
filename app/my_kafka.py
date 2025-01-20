import asyncio
import json

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

# for container
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"

# for local
# KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

TOPIC_NAME = "applications"

producer = None


async def start_kafka_producer():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

    while True:
        try:
            await producer.start()
            break
        except KafkaConnectionError:
            print("Waiting for Kafka to be ready...")
            await asyncio.sleep(1)


async def publish_to_kafka(application):
    message = {
        "id": application.id,
        "user_name": application.user_name,
        "description": application.description,
        "created_at": application.created_at.isoformat(),
    }
    await producer.send_and_wait(
        TOPIC_NAME,
        json.dumps(message).encode("utf-8"),
    )


async def stop_kafka_producer():
    global producer
    await producer.stop()
