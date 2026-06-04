from pydantic import BaseModel, field_validator, Field, EmailStr
from core.utils import hash_password
from schemas.utils import normalize_phone_number
from core.exceptions.validation import AuthDataError

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=15, description="Имя не может быть пустое")
    surname: str = Field(min_length=1, max_length=15, description="Имя не может быть пустое")
    email: EmailStr
    phone: str
    password: str

    @field_validator("password", mode="before")
    @classmethod
    def get_hash_for_password(cls, v):
        if not (8 <= len(v) <= 50):
            raise AuthDataError("Invalid password length")

        upper = lower = digit = False

        for i in v:
            if i.isupper():
                upper = True
            if i.islower():
                lower = True
            if i.isdigit():
                digit = True

        if not (upper and lower and digit):
            raise AuthDataError("Invalid symbol password")

        return hash_password(v).decode('utf-8')


    @field_validator("phone", mode="before")
    @classmethod
    def normalize_phone_number(cls, v):
        return normalize_phone_number(v)

