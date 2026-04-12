from pydantic import BaseModel

class RegisterResponse(BaseModel):
    access_token: str
    refresh_token: str