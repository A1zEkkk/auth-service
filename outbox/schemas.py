from pydantic import BaseModel
from typing import Dict

class RabbitData(BaseModel):
    id: int
    queue_name: str
    message: Dict