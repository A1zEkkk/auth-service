from pydantic import BaseModel



class UserResponseSchema(BaseModel):
    id: int
    login: str
    role: str

