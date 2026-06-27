from fastapi import Depends

from core.rabbit.producer import RabbitProducer, get_rabbit_producer
from aio_pika.exceptions import AMQPError

from core.exc.infrastructure.rabbit import NotificationDeliveryFailed
from outbox.repository import get_outbox_repository


class ProducerService:
    def __init__(self, producer: RabbitProducer):
        self.producer = producer

    async def publish(self, queue_name: str, message: dict):
        try:
            await self.producer.publish(queue_name, message)

        except (AMQPError, TimeoutError, OSError) as e:
                repo = get_outbox_repository()
                await repo.create(queue_name, message)


    async def publish_with_backup(self, queue_name: str, message: dict):
        try:
            await self.producer.publish(queue_name, message)

        except (AMQPError, TimeoutError, OSError) as e:
            raise NotificationDeliveryFailed(
                "Backup timeout"
            ) from e

async def get_producer_service(producer: RabbitProducer = Depends(get_rabbit_producer)):
    return ProducerService(producer)
