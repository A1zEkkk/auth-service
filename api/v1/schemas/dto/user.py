from pydantic import BaseModel, EmailStr

class UserDTO(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    phone: str
    password: str = None

    role: str

    class Config:
        from_attributes = True