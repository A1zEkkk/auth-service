from outbox.repository import OutBoxRepository, get_outbox_repository
from services.producer import ProducerService, NotificationDeliveryFailed, get_rabbit_producer
from .schemas import RabbitData


class OutBoxProcessor:
    def __init__(self, repository: OutBoxRepository, producer: ProducerService):
        self.repository = repository
        self.producer = producer

    async def process_one(self):
        data = await self.repository.get_first()

        if data is None:
            return

        data = RabbitData.model_validate(data)

        try:
            message = await self.producer.publish_with_backup(data.queue_name, data.message)
        except NotificationDeliveryFailed:
            return

        await self.repository.delete(data.id)


def get_outbox_processor() -> OutBoxProcessor:
    repository = get_outbox_repository()
    producer = ProducerService(get_rabbit_producer())
    return OutBoxProcessor(repository, producer)