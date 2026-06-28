from fastapi import Depends

from core.rabbit.producer import RabbitProducer, get_rabbit_producer
from aio_pika.exceptions import AMQPError

from core.exc.infrastructure.rabbit import NotificationDeliveryFailed


class ProducerService:
    def __init__(self, producer: RabbitProducer):
        self.producer = producer

    async def publish(self, queue_name: str, message: dict):
        try:
            await self.producer.publish(queue_name, message)

        except Exception as e:
            raise NotificationDeliveryFailed

async def get_producer_service(producer: RabbitProducer = Depends(get_rabbit_producer)):
    return ProducerService(producer)
