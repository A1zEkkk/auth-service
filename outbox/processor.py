from outbox.repository import OutBoxRepository, get_outbox_repository
from services.producer import ProducerService, NotificationDeliveryFailed, get_rabbit_producer
from .schemas import RabbitData


class OutBoxProcessor:
    def __init__(self, repository: OutBoxRepository, producer: ProducerService):
        self.repository = repository
        self.producer = producer

    async def process_one(self):
        print("Worker tick")

        data = await self.repository.get_first()
        print("Data:", data)

        if data is None:
            print("Outbox is empty")
            return

        print("ID:", data.id)

        data = RabbitData.model_validate(data)
        print("Validated")

        try:
            print("Publishing...")
            await self.producer.publish(
                data.queue_name,
                data.message
            )
            print("Published")
        except NotificationDeliveryFailed:
            print("Publish failed")
            return

        print("Deleting")
        await self.repository.delete(data.id)


def get_outbox_processor() -> OutBoxProcessor:
    repository = get_outbox_repository()
    producer = ProducerService(get_rabbit_producer())
    return OutBoxProcessor(repository, producer)