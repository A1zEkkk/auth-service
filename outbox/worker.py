import asyncio
from .processor import get_outbox_processor

async def run_worker():
    processor = get_outbox_processor()
    while True:
        print("Работаем в нашем цикле")
        await processor.process_one()
        await asyncio.sleep(10)
