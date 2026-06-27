import json
import aio_pika

rabbit_url = "amqp://guest:guest@rabbitmq:5672/"


class RabbitProducer:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()

    async def publish(self, queue_name: str, message: dict):
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode()
            ),
            routing_key=queue_name
        )

    async def close(self):
        await self.connection.close()

rabbit_producer = RabbitProducer(rabbit_url)

def get_rabbit_producer()->RabbitProducer:
    return rabbit_producer