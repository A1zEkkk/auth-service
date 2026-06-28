import json
import aio_pika
from core.configs import settings


class RabbitProducer:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.amqp_url)
            self.channel = await self.connection.channel()
        except Exception as e:
            print(e)
            self.connection = None
            self.channel = None

    async def publish(self, queue_name: str, message: dict):
        if not self.connection or self.connection.is_closed:
            await self.connect()

        if not self.channel or self.channel.is_closed:
            if self.connection:
                self.channel = await self.connection.channel()

        if not self.channel:
            raise RuntimeError("Rabbit channel unavailable")

        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode()
            ),
            routing_key=queue_name
        )

    async def close(self):
        try:
            if self.connection:
                await self.connection.close()
        except Exception:
            pass

rabbit_producer = RabbitProducer(settings.get_broker_url)

def get_rabbit_producer()->RabbitProducer:
    return rabbit_producer