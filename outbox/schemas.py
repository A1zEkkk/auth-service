from pydantic import BaseModel, ConfigDict
from typing import Dict

class RabbitData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    queue_name: str
    message: Dict